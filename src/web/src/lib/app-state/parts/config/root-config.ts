import {debug} from "debug";
import {types} from "mobx-state-tree";

import {AlarmConfig} from "./alarm-config";

const log = debug("weckPiWeb:appState:config");
export const Config = types.model({
    alarm: AlarmConfig
});
