import * as React from "react";
import { Grid } from "@mui/material";
import InfoCard from "./InfoCard";


export default function Dashboard() {
  return (
    <Grid container spacing={2}>
      <InfoCard/>
      <InfoCard/>
      <InfoCard/>
      <InfoCard/>
    </Grid>
  );
}
