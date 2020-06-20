import { Server } from './server';
import * as Logger from 'bunyan';

const log = Logger.createLogger({
    name: 'Test Server',
    level: 'info',
    src: true,
    serializers: Logger.stdSerializers
});

const handleTermination = (eventName: string) => {
    return (): void => {
        server.close(() => {
            process.kill(process.pid, eventName);
        });
    };
};

const handleError = (err: Error): void => {
    log.error(err);
    process.exit(1);
};

export const server = new Server(log, 8080).start();

server.on('error', handleError);
process.on('uncaughtException', handleError);
process.on('unhandledRejection', handleError);
process.once('SIGUSR2', handleTermination('SIGUSR2'));
process.once('SIGINT', handleTermination('SIGINT'));
process.once('SIGTERM', handleTermination('SIGTERM'));
