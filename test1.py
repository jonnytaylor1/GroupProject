import win32print

PRINTER_ERROR_STATES = (
    win32print.PRINTER_STATUS_NO_TONER,
    win32print.PRINTER_STATUS_NOT_AVAILABLE,
    win32print.PRINTER_STATUS_OFFLINE,
    win32print.PRINTER_STATUS_OUT_OF_MEMORY,
    win32print.PRINTER_STATUS_OUTPUT_BIN_FULL,
    win32print.PRINTER_STATUS_PAGE_PUNT,
    win32print.PRINTER_STATUS_PAPER_JAM,
    win32print.PRINTER_STATUS_PAPER_OUT,
    win32print.PRINTER_STATUS_PAPER_PROBLEM,
)


def printer_errorneous_state(printer, error_states=PRINTER_ERROR_STATES):
    prn_opts = win32print.GetPrinter(printer)
    status_opts = prn_opts[18]
    for error_state in error_states:
        if status_opts & error_state:
            return error_state
    return 0


def main():
    printer_name = "Canon Inkjet iP1800 series" # or get_printer_names()[0]
    prn = win32print.OpenPrinter(printer_name)
    error = printer_errorneous_state(prn)
    if error:
        print("ERROR occurred: ", error)
    else:
        print("Printer OK...")
        #  Do the real work

    win32print.ClosePrinter(prn)


if __name__ == "__main__":
    main()
