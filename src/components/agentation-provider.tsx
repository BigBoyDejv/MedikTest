"use client";

import * as React from "react";
import dynamic from "next/dynamic";

const AgentationToolbar = dynamic(
  () => import("agentation").then((mod) => mod.Agentation),
  { ssr: false }
);

export function AgentationProvider() {
  const [isMounted, setIsMounted] = React.useState(false);
  const [isLocalhost, setIsLocalhost] = React.useState(false);

  React.useEffect(() => {
    setIsMounted(true);
    if (
      typeof window !== "undefined" &&
      (window.location.hostname === "localhost" ||
        window.location.hostname === "127.0.0.1")
    ) {
      setIsLocalhost(true);
    }
  }, []);

  // Agentation toolbar sa vykreslí VÝHRADNE na localhoste / v lokálnom vývoji.
  // V produkcii (napr. na Verceli) sa vôbec nenačíta ani nevykreslí.
  if (process.env.NODE_ENV !== "development" || !isMounted || !isLocalhost) {
    return null;
  }

  return <AgentationToolbar />;
}

