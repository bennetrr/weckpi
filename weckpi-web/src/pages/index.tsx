import Head from "next/head";
import React from "react";
import styles from "../styles/Home.module.css";
import nextPackage from "next/package.json";
import TimeView from "../components/TimeView";

export default function Home({}) {
  return (
    <div className={styles.container}>
      <Head>
        <title>WeckPi</title>
        <meta name="charset" content="UTF-8" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className={styles.header_bar}>
        <img src="/weckpi_logo.png" alt="WeckPi Logo" className={styles.logo}/>
        <h1>WeckPi</h1>
      </div>

      <div className={styles.info_view}>
        <TimeView />
      </div>
    </div>
  );
}
