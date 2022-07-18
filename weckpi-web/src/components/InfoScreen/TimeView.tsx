import React, {useEffect, useState} from "react";
import styles from "../../styles/InfoScreen/TimeView.module.css";


import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBell } from '@fortawesome/free-regular-svg-icons'

export default function TimeView({ alarm_time, alarm_day }) {
  const [date, setDate] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setDate(new Date());
    }, 500);

    return () => clearInterval(timer);
  });

  return (
      <div className={styles.time_view}>
        <span className={styles.time}>
          {date.toLocaleTimeString('de-DE')}
        </span>

        <br/>

        <span className={styles.alarm_time}>
          <FontAwesomeIcon icon={faBell} className={styles.bell_icon}/> {alarm_day}, {alarm_time}
        </span>
      </div>
  );
}