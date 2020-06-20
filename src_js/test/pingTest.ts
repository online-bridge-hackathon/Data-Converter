import test from 'ava';
import * as request from 'supertest';
import { Server } from '../src/server';
import * as Logger from 'bunyan';

const log = Logger.createLogger({
    name: 'Test Server',
    level: 'info',
    src: true,
    serializers: Logger.stdSerializers
});

function buildServer(): Server {
  return new Server(log, 8080)
}

test('/ping route', async (t) => {
    return new Promise<void>((resolve) => {
        request(buildServer())
            .get('/ping')
            .set('Accept', 'application/json')
            .expect('Content-Type', /json/)
            .expect(
                200,
                { status: 'OK' },
                (err) => {
                    t.is(err, null);
                    return resolve();
                }
            );
    });
});
