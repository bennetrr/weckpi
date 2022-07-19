import React, {useEffect, useState} from "react";
import styles from "../../styles/Settings/Redirect.module.scss";

import {useRouter} from "next/router";
import Link from "next/link";

export default function SettingsRedirect() {
  const router = useRouter();
  const [isRedirecting, setIsRedirecting] = useState(true);

  useEffect(() => {
    router.push("/settings/alarm_times")
        .then(() => setIsRedirecting(false));
  });

  if (isRedirecting) {
    return (
        <div className={styles.container}>
            <div className={styles.page_content}>
                <p className={styles.text}>
                    Redirecting...
                </p>
            </div>
        </div>
    );
  }
  else {
    return (
        <div className={styles.container}>
          <Link href={"/settings/alarm_times"}>
            <p className={styles.text}>
              Automatic redirect did not work, please click here to go to the settings page manually
            </p>
          </Link>
        </div>
    );
  }
}