*=============================================================================*
* Program: IMPORT.PRG
* System:  RAM FATAKA CENTER Billing Integration
* Target:  Visual FoxPro 6.0 Runtime (Headless / Interactive)
* Purpose: Ingest validated tablet orders from import_staging.json into FAVWIN
*          tables: BILLBOOK, SALEMST, SALETRN, ITEMMST, and LEDGER.
*
* Safety Constraints:
* - Uses native FoxPro engine commands exclusively (100% CDX index safety).
* - Multi-user shared table access (SET EXCLUSIVE OFF).
* - Atomic record locking on sequence counter (BILLBOOK + RLOCK).
* - Multi-tier duplicate protection (Gate 4: SALEMST.NOTE check).
* - Full double-entry accounting ledger generation.
* - Real-time inventory balance updates (ITEMMST.SQTY & CQTY).
* - Rollback and error trapping with audit logging.
*=============================================================================*

LPARAMETERS tcJsonFile
LOCAL lcStagingFile, lcResultFile, lcLogFile
LOCAL lcJsonContent, lnOrderCount, lnSuccessCount, lnSkipCount, lnFailCount
LOCAL llInteractive

* Determine Execution Context
llInteractive = (_VFP.StartMode = 0)

* Default File Paths
IF EMPTY(tcJsonFile)
    lcStagingFile = "import_staging.json"
ELSE
    lcStagingFile = ALLTRIM(tcJsonFile)
ENDIF

lcResultFile = "import_result.json"
lcLogFile    = "import_log.txt"

* Environment Configuration
SET TALK OFF
SET ECHO OFF
SET SAFETY OFF
SET DELETED ON
SET EXACT ON
SET CENTURY ON
SET DATE TO YMD
SET MULTILOCKS ON
SET REPROCESS TO 5 SECONDS
SET EXCLUSIVE OFF

* Initialize Result Buffers
lnOrderCount   = 0
lnSuccessCount = 0
lnSkipCount    = 0
lnFailCount    = 0

=LogMessage("=== BATCH IMPORT STARTED: " + TTOC(DATETIME()) + " ===", lcLogFile)
=LogMessage("Staging File: " + lcStagingFile, lcLogFile)

* Verify Staging File Existence
IF NOT FILE(lcStagingFile)
    =LogMessage("FATAL ERROR: Staging file '" + lcStagingFile + "' not found.", lcLogFile)
    =WriteResultJson(lcResultFile, 0, 0, 0, 1, '[]')
    IF NOT llInteractive
        QUIT
    ENDIF
    RETURN .F.
ENDIF

* Read Staging JSON Content
lcJsonContent = FILETOSTR(lcStagingFile)
IF EMPTY(lcJsonContent)
    =LogMessage("ERROR: Staging file is empty.", lcLogFile)
    =WriteResultJson(lcResultFile, 0, 0, 0, 1, '[]')
    IF NOT llInteractive
        QUIT
    ENDIF
    RETURN .F.
ENDIF

* Open Required Tables in Shared Mode
IF NOT OpenBillingTables(lcLogFile)
    =LogMessage("FATAL ERROR: Failed to open all required database tables.", lcLogFile)
    =WriteResultJson(lcResultFile, 0, 0, 0, 1, '[]')
    IF NOT llInteractive
        QUIT
    ENDIF
    RETURN .F.
ENDIF

* Process Staged Orders
LOCAL lcResultJsonArray
lcResultJsonArray = ""

=ProcessOrderBatch(lcJsonContent, @lnOrderCount, @lnSuccessCount, @lnSkipCount, @lnFailCount, @lcResultJsonArray, lcLogFile)

* Commit Buffers & Close Databases
FLUSH
CLOSE DATABASES

* Write Results JSON
=WriteResultJson(lcResultFile, lnOrderCount, lnSuccessCount, lnSkipCount, lnFailCount, "[" + lcResultJsonArray + "]")

=LogMessage(STRTRAN(STRTRAN("BATCH SUMMARY: Total=<T>, Success=<S>, Skipped=<K>, Failed=<F>", "<T>", STR(lnOrderCount,3)), "<S>", STR(lnSuccessCount,3)), lcLogFile)
=LogMessage("=== BATCH IMPORT COMPLETED: " + TTOC(DATETIME()) + " ===", lcLogFile)

IF NOT llInteractive
    QUIT
ENDIF
RETURN (lnFailCount = 0)


*=============================================================================*
* FUNCTION: OpenBillingTables
* Purpose:  Opens all 5 required billing tables in shared mode with tags.
*=============================================================================*
FUNCTION OpenBillingTables
LPARAMETERS tcLogFile
LOCAL llSuccess
llSuccess = .T.

ON ERROR llSuccess = .F.

* 1. BILLBOOK (Counters)
IF NOT USED("BILLBOOK")
    USE BILLBOOK IN 0 SHARED ORDER CODE
ENDIF

* 2. SALEMST (Invoice Headers)
IF NOT USED("SALEMST")
    USE SALEMST IN 0 SHARED ORDER ENTRY
ENDIF

* 3. SALETRN (Invoice Line Items)
IF NOT USED("SALETRN")
    USE SALETRN IN 0 SHARED ORDER ENTRY
ENDIF

* 4. ITEMMST (Product Inventory)
IF NOT USED("ITEMMST")
    USE ITEMMST IN 0 SHARED ORDER CODE
ENDIF

* 5. LEDGER (Accounting Journal)
IF NOT USED("LEDGER")
    USE LEDGER IN 0 SHARED ORDER ENTRY
ENDIF

ON ERROR

IF NOT (USED("BILLBOOK") AND USED("SALEMST") AND USED("SALETRN") AND USED("ITEMMST") AND USED("LEDGER"))
    =LogMessage("CRITICAL: One or more DBF files could not be opened in SHARED mode.", tcLogFile)
    RETURN .F.
ENDIF

RETURN .T.


*=============================================================================*
* FUNCTION: ProcessOrderBatch
* Purpose:  Parses JSON orders array and converts each order into FoxPro tables.
*=============================================================================*
FUNCTION ProcessOrderBatch
LPARAMETERS tcJson, rnTotal, rnSuccess, rnSkip, rnFail, rcResultArray, tcLogFile

LOCAL lnOrdersStart, lcOrdersText, lnPos, lcOrderBlock, lnBlockEnd
LOCAL lcOrderId, lcDraftId, lcCustCode, lcCustName, lcOrderDate, lcAcode
LOCAL lnGross, lnAdd, lnLess, lnRoff, lnNet, lcUser, lcSalesman, lcNote, lcRemarks
LOCAL lnNewEntry, llOrderSuccess, lcOrderResultJson
LOCAL ldDate

rnTotal = 0
rnSuccess = 0
rnSkip = 0
rnFail = 0
rcResultArray = ""

* Locate the "orders": [ array
lnOrdersStart = AT('"orders"', tcJson)
IF lnOrdersStart = 0
    lnOrdersStart = AT("'orders'", tcJson)
ENDIF

IF lnOrdersStart = 0
    =LogMessage("No 'orders' key found in JSON payload.", tcLogFile)
    RETURN
ENDIF

lcOrdersText = SUBSTR(tcJson, lnOrdersStart)

* Scan for each order object by draft_id or order_id
lnPos = AT('"draft_id"', lcOrdersText)
DO WHILE lnPos > 0
    * Find bounding brace before "draft_id"
    LOCAL lnStartBrace, lnDepth, lnCharIdx, lcChar
    lnStartBrace = RAT('{', SUBSTR(lcOrdersText, 1, lnPos))
    
    * Extract JSON object
    lnDepth = 0
    lnBlockEnd = 0
    FOR lnCharIdx = lnStartBrace TO LEN(lcOrdersText)
        lcChar = SUBSTR(lcOrdersText, lnCharIdx, 1)
        IF lcChar = '{'
            lnDepth = lnDepth + 1
        ELSE
            IF lcChar = '}'
                lnDepth = lnDepth - 1
                IF lnDepth = 0
                    lnBlockEnd = lnCharIdx
                    EXIT
                ENDIF
            ENDIF
        ENDIF
    ENDFOR
    
    IF lnBlockEnd > lnStartBrace
        lcOrderBlock = SUBSTR(lcOrdersText, lnStartBrace, lnBlockEnd - lnStartBrace + 1)
        
        * Parse Header Fields
        lcOrderId   = ExtractJsonVal(lcOrderBlock, "order_id")
        lcDraftId   = ExtractJsonVal(lcOrderBlock, "draft_id")
        lcCustCode  = PADR(ExtractJsonVal(lcOrderBlock, "customer_code"), 5)
        lcCustName  = PADR(ExtractJsonVal(lcOrderBlock, "customer_name"), 40)
        lcOrderDate = ExtractJsonVal(lcOrderBlock, "order_date")
        lcAcode     = PADR(ExtractJsonVal(lcOrderBlock, "area_code"), 5)
        lnGross     = VAL(ExtractJsonVal(lcOrderBlock, "gross_amount"))
        lnAdd       = VAL(ExtractJsonVal(lcOrderBlock, "add_amount"))
        lnLess      = VAL(ExtractJsonVal(lcOrderBlock, "less_amount"))
        lnRoff      = VAL(ExtractJsonVal(lcOrderBlock, "round_off"))
        lnNet       = VAL(ExtractJsonVal(lcOrderBlock, "net_amount"))
        lcUser      = PADR(ExtractJsonVal(lcOrderBlock, "user"), 10)
        lcSalesman  = PADR(ExtractJsonVal(lcOrderBlock, "salesman"), 5)
        lcRemarks   = PADR(ExtractJsonVal(lcOrderBlock, "remarks"), 25)
        
        IF EMPTY(lcUser)
            lcUser = "RAM       "
        ENDIF
        IF EMPTY(lcSalesman)
            lcSalesman = "SELF "
        ENDIF
        
        lcNote = PADR("DRAFT:" + ALLTRIM(lcDraftId), 40)
        
        * Convert Date String YYYYMMDD to Date
        IF LEN(ALLTRIM(lcOrderDate)) >= 8
            ldDate = DATE(VAL(SUBSTR(lcOrderDate,1,4)), VAL(SUBSTR(lcOrderDate,5,2)), VAL(SUBSTR(lcOrderDate,7,2)))
        ELSE
            ldDate = DATE()
        ENDIF
        
        rnTotal = rnTotal + 1
        
        * Gate 4 Duplicate Check: Verify SALEMST.NOTE
        SELECT SALEMST
        LOCATE FOR ALLTRIM(NOTE) == "DRAFT:" + ALLTRIM(lcDraftId)
        IF FOUND()
            =LogMessage("GATE 4 SKIPPED: Draft " + lcDraftId + " already imported as ENTRY " + ALLTRIM(STR(SALEMST.ENTRY)), tcLogFile)
            rnSkip = rnSkip + 1
            lcOrderResultJson = '{"order_id":"' + lcOrderId + '","draft_id":"' + lcDraftId + '","status":"SKIPPED","legacy_entry_no":' + ALLTRIM(STR(SALEMST.ENTRY)) + ',"message":"Duplicate draft ID"}'
        ELSE
            * Attempt Import Transaction
            lnNewEntry = 0
            llOrderSuccess = ImportSingleInvoice(lcOrderBlock, lcOrderId, lcDraftId, lcCustCode, lcCustName, ldDate, ;
                                                lcAcode, lnGross, lnAdd, lnLess, lnRoff, lnNet, lcUser, lcSalesman, lcNote, lcRemarks, ;
                                                @lnNewEntry, tcLogFile)
            
            IF llOrderSuccess
                rnSuccess = rnSuccess + 1
                =LogMessage("SUCCESS: Draft " + lcDraftId + " imported as Invoice #" + ALLTRIM(STR(lnNewEntry)), tcLogFile)
                lcOrderResultJson = '{"order_id":"' + lcOrderId + '","draft_id":"' + lcDraftId + '","status":"SUCCESS","legacy_entry_no":' + ALLTRIM(STR(lnNewEntry)) + ',"message":"Created successfully"}'
            ELSE
                rnFail = rnFail + 1
                =LogMessage("FAILED: Draft " + lcDraftId + " failed during processing.", tcLogFile)
                lcOrderResultJson = '{"order_id":"' + lcOrderId + '","draft_id":"' + lcDraftId + '","status":"FAILED","legacy_entry_no":0,"message":"Import transaction aborted"}'
            ENDIF
        ENDIF
        
        IF EMPTY(rcResultArray)
            rcResultArray = lcOrderResultJson
        ELSE
            rcResultArray = rcResultArray + "," + CHR(13) + CHR(10) + lcOrderResultJson
        ENDIF
        
        * Advance to next order in text
        lcOrdersText = SUBSTR(lcOrdersText, lnBlockEnd + 1)
        lnPos = AT('"draft_id"', lcOrdersText)
    ELSE
        EXIT
    ENDIF
ENDDO


*=============================================================================*
* FUNCTION: ImportSingleInvoice
* Purpose:  Executes transactional steps for one invoice across all tables.
*=============================================================================*
FUNCTION ImportSingleInvoice
LPARAMETERS tcOrderBlock, tcOrderId, tcDraftId, tcCustCode, tcCustName, tdDate, ;
            tcAcode, tnGross, tnAdd, tnLess, tnRoff, tnNet, tcUser, tcSalesman, tcNote, tcRemarks, ;
            rnAssignedEntry, tcLogFile

LOCAL lnEntry, llLocked, lnItemCount, lcItemsText, lnItemsStart, lnItemPos
LOCAL lcItemBlock, lnItemEnd, lnItemDepth, lnIdx, lcChar
LOCAL lcICode, lcGCode, lcCCode, lcUnit, lcRttp, lnQty, lnRate, lnGrossItem, lcTCode, lnTaxPct, lnTaxable, lnNetItem
LOCAL ARRAY laInsertedItems[500, 2]  && Tracks inserted (icode, qty) for rollback

rnAssignedEntry = 0
lnItemCount = 0

* Step 1: Reserve Next Invoice Number in BILLBOOK
SELECT BILLBOOK
LOCATE FOR ALLTRIM(CODE) == "E"
IF NOT FOUND()
    =LogMessage("ERROR: Series 'E' not found in BILLBOOK.DBF", tcLogFile)
    RETURN .F.
ENDIF

* Obtain Lock on BILLBOOK
llLocked = .F.
FOR lnTry = 1 TO 10
    IF RLOCK()
        llLocked = .T.
        EXIT
    ENDIF
    =INKEY(0.2)
ENDFOR

IF NOT llLocked
    =LogMessage("ERROR: Timeout acquiring lock on BILLBOOK.DBF for Draft " + tcDraftId, tcLogFile)
    RETURN .F.
ENDIF

lnEntry = BILLBOOK.ENTRY + 1
REPLACE BILLBOOK.ENTRY WITH lnEntry
UNLOCK

rnAssignedEntry = lnEntry
=LogMessage("Assigned Invoice Entry: " + ALLTRIM(STR(lnEntry)) + " for Draft: " + tcDraftId, tcLogFile)

* Step 2: Insert Line Items into SALETRN & Deduct Inventory in ITEMMST
lnItemsStart = AT('"items"', tcOrderBlock)
IF lnItemsStart = 0
    =LogMessage("ERROR: No 'items' array in order " + tcDraftId, tcLogFile)
    =RollbackInvoice(lnEntry, 0, laInsertedItems, tcLogFile)
    RETURN .F.
ENDIF

lcItemsText = SUBSTR(tcOrderBlock, lnItemsStart)
lnItemPos = AT('"item_code"', lcItemsText)

DO WHILE lnItemPos > 0
    LOCAL lnStartItemBrace
    lnStartItemBrace = RAT('{', SUBSTR(lcItemsText, 1, lnItemPos))
    
    lnItemDepth = 0
    lnItemEnd = 0
    FOR lnIdx = lnStartItemBrace TO LEN(lcItemsText)
        lcChar = SUBSTR(lcItemsText, lnIdx, 1)
        IF lcChar = '{'
            lnItemDepth = lnItemDepth + 1
        ELSE
            IF lcChar = '}'
                lnItemDepth = lnItemDepth - 1
                IF lnItemDepth = 0
                    lnItemEnd = lnIdx
                    EXIT
                ENDIF
            ENDIF
        ENDIF
    ENDFOR
    
    IF lnItemEnd > lnStartItemBrace
        lcItemBlock = SUBSTR(lcItemsText, lnStartItemBrace, lnItemEnd - lnStartItemBrace + 1)
        
        lcICode     = PADR(ExtractJsonVal(lcItemBlock, "item_code"), 5)
        lcGCode     = PADR(ExtractJsonVal(lcItemBlock, "group_code"), 5)
        lcCCode     = PADR(ExtractJsonVal(lcItemBlock, "company_code"), 5)
        lcUnit      = PADR(ExtractJsonVal(lcItemBlock, "unit"), 5)
        lcRttp      = PADR(ExtractJsonVal(lcItemBlock, "rate_type"), 1)
        lnQty       = VAL(ExtractJsonVal(lcItemBlock, "quantity"))
        lnRate      = VAL(ExtractJsonVal(lcItemBlock, "rate"))
        lnGrossItem = VAL(ExtractJsonVal(lcItemBlock, "gross_amount"))
        lcTCode     = PADR(ExtractJsonVal(lcItemBlock, "tax_code"), 5)
        lnTaxPct    = VAL(ExtractJsonVal(lcItemBlock, "tax_percent"))
        lnTaxable   = VAL(ExtractJsonVal(lcItemBlock, "taxable_amount"))
        lnNetItem   = VAL(ExtractJsonVal(lcItemBlock, "net_amount"))
        
        IF EMPTY(lcUnit)
            lcUnit = "PKT  "
        ENDIF
        IF EMPTY(lcRttp)
            lcRttp = "P"
        ENDIF
        IF EMPTY(lcTCode)
            lcTCode = "CST  "
        ENDIF
        
        * Append Line Item to SALETRN
        SELECT SALETRN
        APPEND BLANK
        REPLACE ENTRY WITH lnEntry, ;
                COME  WITH "E ", ;
                CD    WITH "D", ;
                DATE  WITH tdDate, ;
                PCODE WITH tcCustCode, ;
                ACODE WITH tcAcode, ;
                SCODE WITH tcSalesman, ;
                ICODE WITH lcICode, ;
                GCODE WITH lcGCode, ;
                CCODE WITH lcCCode, ;
                QTY   WITH lnQty, ;
                RATE  WITH lnRate, ;
                RTTP  WITH lcRttp, ;
                GAMT  WITH lnGrossItem, ;
                TCODE WITH lcTCode, ;
                TAXP  WITH lnTaxPct, ;
                TAMT  WITH lnTaxable, ;
                NAMT  WITH lnNetItem, ;
                USER  WITH tcUser, ;
                UNIT  WITH lcUnit
        
        * Update Inventory in ITEMMST
        SELECT ITEMMST
        SEEK lcICode
        IF FOUND()
            IF RLOCK()
                REPLACE SQTY WITH SQTY + lnQty, ;
                        CQTY WITH CQTY - lnQty
                UNLOCK
            ELSE
                =LogMessage("WARNING: Could not lock ITEMMST for " + lcICode + ", stock not updated", tcLogFile)
            ENDIF
        ELSE
            =LogMessage("WARNING: Product " + lcICode + " not found in ITEMMST.DBF", tcLogFile)
        ENDIF
        
        * Record for Rollback Tracking
        lnItemCount = lnItemCount + 1
        IF lnItemCount <= 500
            laInsertedItems[lnItemCount, 1] = lcICode
            laInsertedItems[lnItemCount, 2] = lnQty
        ENDIF
        
        lcItemsText = SUBSTR(lcItemsText, lnItemEnd + 1)
        lnItemPos = AT('"item_code"', lcItemsText)
    ELSE
        EXIT
    ENDIF
ENDDO

IF lnItemCount = 0
    =LogMessage("ERROR: Zero valid line items parsed for " + tcDraftId, tcLogFile)
    =RollbackInvoice(lnEntry, lnItemCount, laInsertedItems, tcLogFile)
    RETURN .F.
ENDIF

* Step 3: Insert Invoice Header into SALEMST
SELECT SALEMST
APPEND BLANK
REPLACE ENTRY   WITH lnEntry, ;
        COME    WITH "E ", ;
        DATE    WITH tdDate, ;
        PCODE   WITH tcCustCode, ;
        SCODE   WITH tcSalesman, ;
        CD      WITH "D", ;
        T4A     WITH tnGross, ;
        ADD     WITH tnAdd, ;
        LESS    WITH tnLess, ;
        ROFF    WITH tnRoff, ;
        NAMT    WITH tnNet, ;
        USER    WITH tcUser, ;
        PNAME   WITH tcCustName, ;
        NOTE    WITH tcNote, ;
        REMA    WITH tcRemarks

* Step 4: Insert Double-Entry Bookkeeping into LEDGER
LOCAL lcNarration
lcNarration = PADR("INV.NO.E / " + STR(lnEntry, 5), 40)

SELECT LEDGER

* 4A. Debtor Debit (Customer Account Debited)
APPEND BLANK
REPLACE ENTRY   WITH lnEntry, ;
        COME    WITH "E ", ;
        DATE    WITH tdDate, ;
        DCODE   WITH tcCustCode, ;
        CCODE   WITH "     ", ;
        NHEAD   WITH "S0   ", ;
        AMOUNT  WITH tnNet, ;
        NARA1   WITH lcNarration, ;
        IND     WITH "SL", ;
        USER    WITH tcUser

* 4B. Sales Revenue Credit (Sales Account Credited)
APPEND BLANK
REPLACE ENTRY   WITH lnEntry, ;
        COME    WITH "E ", ;
        DATE    WITH tdDate, ;
        DCODE   WITH "     ", ;
        CCODE   WITH "S4   ", ;
        NHEAD   WITH tcCustCode, ;
        AMOUNT  WITH tnNet, ;
        NARA1   WITH lcNarration, ;
        IND     WITH "SL", ;
        USER    WITH tcUser

RETURN .T.


*=============================================================================*
* FUNCTION: RollbackInvoice
* Purpose:  Cleans up partially written rows and reverts stock on failure.
*=============================================================================*
FUNCTION RollbackInvoice
LPARAMETERS tnEntry, tnItemCount, taItems, tcLogFile
LOCAL lnI, lcItemCode, lnQty

=LogMessage("INITIATING ROLLBACK for Entry #" + ALLTRIM(STR(tnEntry)), tcLogFile)

* 1. Revert Inventory Deductions in ITEMMST
IF tnItemCount > 0
    SELECT ITEMMST
    FOR lnI = 1 TO tnItemCount
        lcItemCode = taItems[lnI, 1]
        lnQty      = taItems[lnI, 2]
        IF NOT EMPTY(lcItemCode)
            SEEK lcItemCode
            IF FOUND()
                IF RLOCK()
                    REPLACE SQTY WITH SQTY - lnQty, ;
                            CQTY WITH CQTY + lnQty
                    UNLOCK
                ENDIF
            ENDIF
        ENDIF
    ENDFOR
ENDIF

* 2. Mark SALETRN lines as deleted
SELECT SALETRN
DELETE FOR ENTRY = tnEntry AND ALLTRIM(COME) == "E"

* 3. Mark SALEMST header as deleted
SELECT SALEMST
DELETE FOR ENTRY = tnEntry AND ALLTRIM(COME) == "E"

* 4. Mark LEDGER entries as deleted
SELECT LEDGER
DELETE FOR ENTRY = tnEntry AND ALLTRIM(COME) == "E"

* 5. Revert BILLBOOK sequence counter if this was the last assigned
SELECT BILLBOOK
LOCATE FOR ALLTRIM(CODE) == "E"
IF FOUND()
    IF BILLBOOK.ENTRY = tnEntry
        IF RLOCK()
            REPLACE BILLBOOK.ENTRY WITH tnEntry - 1
            UNLOCK
            =LogMessage("Rolled back BILLBOOK.ENTRY to " + ALLTRIM(STR(tnEntry - 1)), tcLogFile)
        ENDIF
    ENDIF
ENDIF

=LogMessage("ROLLBACK COMPLETED for Entry #" + ALLTRIM(STR(tnEntry)), tcLogFile)
RETURN .T.


*=============================================================================*
* HELPER: ExtractJsonVal
* Purpose: Extracts string/number value for a given key from JSON fragment.
*=============================================================================*
FUNCTION ExtractJsonVal
LPARAMETERS tcBlock, tcKey
LOCAL lnKeyPos, lcSub, lnColonPos, lnQuote1, lnQuote2, lnEndPos, lcVal

lnKeyPos = AT('"' + tcKey + '"', tcBlock)
IF lnKeyPos = 0
    lnKeyPos = AT("'" + tcKey + "'", tcBlock)
ENDIF

IF lnKeyPos = 0
    RETURN ""
ENDIF

lcSub = SUBSTR(tcBlock, lnKeyPos + LEN(tcKey) + 2)
lnColonPos = AT(':', lcSub)
IF lnColonPos = 0
    RETURN ""
ENDIF

lcSub = ALLTRIM(SUBSTR(lcSub, lnColonPos + 1))

* If value is a quoted string
IF SUBSTR(lcSub, 1, 1) = '"'
    lnQuote2 = AT('"', SUBSTR(lcSub, 2))
    IF lnQuote2 > 0
        RETURN SUBSTR(lcSub, 2, lnQuote2 - 1)
    ENDIF
ENDIF

* If value is numeric, boolean, or null (delimited by comma, newline, or brace)
lnEndPos = LEN(lcSub)
LOCAL lnComma, lnBrace
lnComma = AT(',', lcSub)
lnBrace = AT('}', lcSub)

IF lnComma > 0 AND lnComma < lnEndPos
    lnEndPos = lnComma
ENDIF
IF lnBrace > 0 AND lnBrace < lnEndPos
    lnEndPos = lnBrace
ENDIF

lcVal = ALLTRIM(SUBSTR(lcSub, 1, lnEndPos - 1))
lcVal = CHRTRAN(lcVal, CHR(13) + CHR(10) + CHR(9), "")
RETURN ALLTRIM(lcVal)


*=============================================================================*
* HELPER: LogMessage
* Purpose: Appends timestamped line to import log file.
*=============================================================================*
FUNCTION LogMessage
LPARAMETERS tcMsg, tcLogFile
LOCAL lcLine
lcLine = "[" + TTOC(DATETIME()) + "] " + tcMsg + CHR(13) + CHR(10)
=STRTOFILE(lcLine, tcLogFile, 1)
? tcMsg
RETURN .T.


*=============================================================================*
* HELPER: WriteResultJson
* Purpose: Writes structured import result file for Python Sync Service.
*=============================================================================*
FUNCTION WriteResultJson
LPARAMETERS tcResultFile, tnTotal, tnSuccess, tnSkip, tnFail, tcOrdersJson
LOCAL lcJson
lcJson = "{" + CHR(13) + CHR(10) + ;
         '  "completed_at": "' + TTOC(DATETIME()) + '",' + CHR(13) + CHR(10) + ;
         '  "total_orders": ' + ALLTRIM(STR(tnTotal)) + ',' + CHR(13) + CHR(10) + ;
         '  "success_count": ' + ALLTRIM(STR(tnSuccess)) + ',' + CHR(13) + CHR(10) + ;
         '  "skipped_count": ' + ALLTRIM(STR(tnSkip)) + ',' + CHR(13) + CHR(10) + ;
         '  "failed_count": ' + ALLTRIM(STR(tnFail)) + ',' + CHR(13) + CHR(10) + ;
         '  "results": ' + tcOrdersJson + CHR(13) + CHR(10) + ;
         "}"
=STRTOFILE(lcJson, tcResultFile, 0)
RETURN .T.
