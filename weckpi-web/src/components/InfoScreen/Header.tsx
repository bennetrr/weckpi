import React from "react";
import styles from "../../styles/Header.module.scss";

import {faCog} from "@fortawesome/free-solid-svg-icons";
import MenuEntry from "../MenuEntry";

function MenuProductEntry() {
    return (
        <div className={styles.menuItemNonInteractive}>
            <img src={"/weckpi_logo.png"} className={styles.menuProductEntryIcon} alt={"WeckPi Logo"}/>
            <span className={styles.menuProductEntryText}><b>WeckPi</b></span>
        </div>
    )
}

export default function Header() {
    return (
        <div className={styles.header}>
            <MenuProductEntry />
            <div className={styles.leftRightSep} />
            <MenuEntry link={"/settings"} icon={faCog} />
        </div>
    );
}