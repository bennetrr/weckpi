import React from "react";
import styles from "../../styles/Home.module.css";

import Head from "next/head";
import Header from "../../components/Settings/Header";

export default function Home({}) {
  return (
    <div className={styles.container}>
      <Head>
        <title>WeckPi Settings</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />
      <div style={{ flex: 1 }} />

    </div>
  );
}