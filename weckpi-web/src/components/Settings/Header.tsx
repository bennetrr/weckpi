import React from "react";
import styles from "../../styles/Header.module.scss";

import MenuEntry from "../MenuEntry";
import {faHome, faBell, faMusic, faSave} from "@fortawesome/free-solid-svg-icons";
import {useRouter} from "next/router";

function Seperator() {
    return <div className={styles.seperator}/>;
}

function MenuProductEntry() {
    return (
        <div className={styles.menuItemNonInteractive}>
            <img src={"/weckpi_logo.png"} className={styles.menuProductEntryIcon} alt={"WeckPi Logo"}/>
            <span className={styles.menuProductEntryText}><b>WeckPi</b> Settings</span>
        </div>
    )
}

export default function Header() {
    const router = useRouter();
    const activeRoute = router.pathname.replace("/settings/", "");

    return (
        <div className={styles.header}>
            <MenuProductEntry />
            <Seperator/>

            <MenuEntry text={"Alarm Times"} icon={faBell} link={"/settings/alarm_times"} active={activeRoute==="alarm_times"} />
            <MenuEntry text={"Music"} icon={faMusic} link={"/settings/music"} active={activeRoute==="music"} />

            <div className={styles.leftRightSep} />

            <MenuEntry link={"/"} icon={faSave} />
            <MenuEntry link={"/"} icon={faHome} />
        </div>
    );
}