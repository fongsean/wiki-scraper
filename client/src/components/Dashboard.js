import React, { useState, useEffect } from "react";
import { Grid } from "@mui/material";
import InfoCard from "./InfoCard";

export default function Dashboard() {
  const [wikiDetails, setWikiDetails] = useState({ vCards: [0, 1, 2] });

  useEffect(() => {
    fetch("/crawl")
      .then((res) => res.json())
      .then((data) => {
        setWikiDetails(data);
      });
  }, []);

  return (
    <Grid container spacing={2}>
      {wikiDetails.vCards.map((vCard, idx) => {
        return <InfoCard key={idx} vCard={vCard} />;
      })}
    </Grid>
  );
}
