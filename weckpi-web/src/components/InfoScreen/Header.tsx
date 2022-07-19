import React from "react";
import styles from "../../styles/Header.module.scss";

import Link from "next/link";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCog} from "@fortawesome/free-solid-svg-icons";

export default function Header() {
  return (
      <div className={styles.header}>
        <img src={"/weckpi_logo.png"} alt={"WeckPi Logo"} className={styles.logo}/>
        <p className={styles.product_name}>WeckPi</p>
        <Link href={"/settings"}>
          <FontAwesomeIcon icon={faCog} className={styles.page_switch_button}/>
        </Link>
      </div>
  );
}