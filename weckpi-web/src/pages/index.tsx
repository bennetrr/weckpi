import React from "react";
import styles from "../styles/Page.module.scss";

import Head from "next/head";
import InfoView from "../components/InfoScreen/InfoView";
import Header from "../components/InfoScreen/Header";
import MusicBar from "../components/InfoScreen/MusicBar";

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>WeckPi</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />
      <InfoView alarm_time={"8:30"} alarm_day={"Morgen"} />
      <MusicBar />

    </div>
  );
}
