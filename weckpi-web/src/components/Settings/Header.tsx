import React from "react";
import styles from "../../styles/Header.module.scss";

import Link from "next/link";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faHome} from "@fortawesome/free-solid-svg-icons";

export function Seperator() {
  return (
    <div className={styles.seperator} />
  );
}

export default function Header() {
  return (
      <div className={styles.header}>
        <img src={"/weckpi_logo.png"} alt={"WeckPi Logo"} className={styles.logo}/>
        <span className={styles.product_name}>WeckPi</span><span className={styles.settings_text}>Settings</span>
        <Seperator />
        <Link href={"/"}>
          <FontAwesomeIcon icon={faHome} className={styles.page_switch_button}/>
        </Link>
      </div>
  );
}