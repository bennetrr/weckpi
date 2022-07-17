import React, {useState, useEffect} from "react";
import styles from "../styles/TimeView.module.css";

export default function TimeView() {
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
          {date.toLocaleTimeString()}
        </span>
      </div>
  );
}