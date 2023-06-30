import {io, type Socket} from "socket.io-client";
import {writable} from "svelte/store";

export const weckpiCore = writable<WeckPiCoreConnection>();

export class WeckPiCoreConnection {
    private sio: Socket;
    private disabled: boolean;

    public constructor() {
        this.sio = io("ws://localhost:8000/");
        this.disabled = true;
    }

    public enable() {
        this.disabled = false;
    }

    public getInitialData(fn: (initialData: any) => void) {
        this.sio.emit("initial-data-request", fn)
    }

    public propertyChange(prop: string, value: any) {
        if (this.disabled) return;
        this.sio.emit("property-change", {prop, value});
    }

    public onPropertyChange(fn: (prop: string, value: any) => void) {
        this.sio.on("property-change", (args) => fn(args.prop, args.value));
    }

    public action(name: string) {
        if (this.disabled) return;
        this.sio.emit("action", {name});
    }
}
