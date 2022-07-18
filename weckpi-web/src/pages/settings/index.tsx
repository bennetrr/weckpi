import React, {useEffect, useState} from "react";
import {useRouter} from "next/router";
import Link from "next/link";

export default function Settings() {
  const router = useRouter();
  const [isRedirecting, setIsRedirecting] = useState(true);

  useEffect(() => {
    router.push("/settings/alarm_times")
        .then(() => setIsRedirecting(false));
  });

  if (isRedirecting) {
    return (
        <div style={{ height: "100vh", backgroundColor: "#252525", color: "#fff" }}>
          <p style={{ width: "100vw", textAlign: "center" }}>
            Redirecting...
          </p>
        </div>
    );
  }
  else {
    return (
        <div style={{ height: "100vh", backgroundColor: "#252525", color: "#fff" }}>
          <Link href={"/settings/alarm_times"}>
            <p style={{ width: "100vw", textAlign: "center" }}>
              Automatic redirect did not work, please click here to go to the settings page manually
            </p>
          </Link>
        </div>
    );
  }
}