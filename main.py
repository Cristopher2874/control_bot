import logging

from app.orchestrator import run_bot

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    run_bot()
    logger.info("Stopped application\n\n\n")