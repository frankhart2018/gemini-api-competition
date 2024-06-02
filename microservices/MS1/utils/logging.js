const LogLevel = Object.freeze({
    INFO: 'INFO',
    WARN: 'WARN',
    ERROR: 'ERROR'
});

class Logger {
    constructor(loggerUrl, loggerToken) {
        if (!Logger.instance) {
            this.loggerUrl = loggerUrl;
            this.loggerToken = loggerToken;
            Logger.instance = this;
        }
    }

    log(level, message) {
        if (!this.loggerUrl || !this.loggerToken) {
            console.error('Logger not initialized. Please set the LOGGER_URL and LOGGER_TOKEN environment variables.');
            return;
        }

        const currentTime = new Date().toLocaleString();
        const formattedTime = currentTime.replace('T', ' ').replace('Z', '');

        const log = {
            "dt": formattedTime,
            "message": `${level}: ${message}`
        };

        fetch(this.loggerUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.loggerToken}`,
            },
            body: JSON.stringify(log)
        }).then((response) => {
            if (response.status !== 202) {
                console.error(`Failed to log message: ${message}`);
            }
        })
    }
}

const logger = new Logger(process.env.LOGGER_URL, process.env.LOGGER_TOKEN);
Object.freeze(logger);

export { logger, LogLevel };
