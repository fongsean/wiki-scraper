import React from "react";
import { Box, Card, CardActions, CardContent, Button, Typography, Grid } from "@mui/material";

export default function InfoCard(props) {
  const { title, vCardData } = props.vCard

  for (const [key, value] of Object.entries(vCardData)) {
    console.log(`${key}: ${value}`);
  }

  return (
    <Grid item xs={3}>
      <Card>
        <CardContent>
          <Typography variant="h5" component="div" sx={{ mb: 1.5 }}>
            {title}
          </Typography>
          <Typography variant="body2">
            well meaning and kindly.
            <br />
            {'"a benevolent smile"'}
          </Typography>
        </CardContent>
        <CardActions>
          <Button size="small">Learn More</Button>
        </CardActions>
      </Card>
    </Grid>
  );
}
