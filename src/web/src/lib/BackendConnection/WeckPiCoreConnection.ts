export interface MessageData {
    propertyName: string;
    value: any;
}

export default class WeckPiCoreConnection {
    private webSocket: WebSocket;

    public constructor(url: string) {
        this.webSocket = new WebSocket(url);
    }

    public send(data: MessageData) {
        this.webSocket.send(JSON.stringify(data));
    }

    public close() {
        this.webSocket.close(1001);
    }

    public setOnMessage(func: (event: MessageEvent) => void, overwrite: boolean = false) {
        if (this.webSocket.onmessage !== undefined && !overwrite) return;
        this.webSocket.onmessage = func;
    }
}
