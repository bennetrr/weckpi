import React from "react";
import styles from "../../styles/Page.module.scss";

import Head from "next/head";
import Header from "../../components/Settings/Header";

export default function AlarmTimesSettings() {
  return (
    <div className={styles.container}>
      <Head>
        <title>WeckPi Settings: Alarm Times</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />
      <div className={styles.page_content}>

      </div>
    </div>
  );
}