from qqyklog import qqyk_debug
if __name__=="__main__":

    log=qqyk_debug()
    log.debug("DEBUG")
    log.info("INFO")
    log.warning("WARNING")
    log.critical("CRITICAL")
    log.error("ERROR")