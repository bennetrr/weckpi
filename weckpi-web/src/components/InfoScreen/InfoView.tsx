import React from "react";
import styles from "../../styles/InfoScreen/InfoView.module.scss";

import TimeView from "./TimeView";
import InfoViewProps from "../../types/InfoViewProps";

export default function InfoView({alarm_time, alarm_day}: InfoViewProps) {
  return (<div className={styles.info_view}>
        <TimeView alarm_time={alarm_time} alarm_day={alarm_day}/>
      </div>)
}