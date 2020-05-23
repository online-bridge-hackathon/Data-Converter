import * as Http from 'http';
import * as Logger from 'bunyan';
const express = require('express')

export class Server {
    public app;
    public server: Http.Server;
    private log: Logger;
    private port: number;

    constructor(log: Logger, port: number) {
        this.app = express();
        this.log = log;
        this.port = port;

        this.app.get('/ping', (_req, res) => {
            return res.status(200).send({
                status: 'OK'
            });
        });

        this.server = Http.createServer(this.app);
        this.server.on('listening', () => {
            this.log.info(`Server listening on port ${port}`);
        });
    }

    public start(): Http.Server {
        this.server.listen(this.port);
        return this.server;
    }
}
