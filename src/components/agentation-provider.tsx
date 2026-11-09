"use client";

import * as React from "react";
import dynamic from "next/dynamic";

const AgentationToolbar = dynamic(
  () => import("agentation").then((mod) => mod.Agentation),
  { ssr: false }
);

export function AgentationProvider() {
  const [isMounted, setIsMounted] = React.useState(false);

  React.useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return null;
  }

  // Render in development or whenever requested
  return <AgentationToolbar />;
}
