import React from "react";
import styles from "../../styles/InfoScreen/InfoView.module.css";
import TimeView from "./TimeView";

export default function InfoView({ alarm_time, alarm_day }) {
  return (
      <div className={styles.info_view}>
        <TimeView alarm_time={alarm_time} alarm_day={alarm_day} />
      </div>
  )
}