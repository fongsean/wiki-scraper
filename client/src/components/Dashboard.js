import React, { useState, useEffect } from "react";
import { Grid } from "@mui/material";
import InfoCard from "./InfoCard";

export default function Dashboard() {
  const [wikiDetails, setWikiDetails] = useState({ wikiData: ["Placeholder"] });

  useEffect(() => {
    fetch("/scrapwiki")
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setWikiDetails(data);
      });
  }, []);

  return (
    <Grid container spacing={2} sx={{ mt: 2 }}>
      {wikiDetails.wikiData.map((pageData, idx) => {
        return <InfoCard key={idx} pageData={pageData} />;
      })}
    </Grid>
  );
}
