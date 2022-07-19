import React from "react";
import styles from "../styles/Header.module.scss";
import MenuEntryProps from "../types/MenuEntryProps";

import Link from "next/link";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

export default function MenuEntry({text, icon, link, active}: MenuEntryProps) {
    if (text === undefined && icon === undefined) throw new Error("MenuEntry: text or icon (or both) must be given!");

    const styleName = active ? styles.menuItemActive : styles.menuItem;

    return (
        <Link href={link}>
            <div className={styleName}>
                {icon === undefined ? <></> : <FontAwesomeIcon icon={icon} className={styles.menuItemIcon}/>}
                {text === undefined ? <></> : <span className={styles.menuItemText}>{text}</span>}
            </div>
        </Link>
    );
}