import React from "react";
import { Card, CardActions, CardContent, Button, Typography, Grid } from "@mui/material";

export default function InfoCard(props) {
  const { title, category, url, scores } = props.pageData;

  var hasScore = typeof scores !== "undefined";

  if (hasScore) {
    // convert object to [category, score] array
    const sortable = [];
    for (const category in scores) {
      sortable.push([category, scores[category]]);
    }

    // sort array based on score value
    sortable.sort(function (scoreA, scoreB) {
      return scoreB[1] - scoreA[1];
    });
    var top3scores = sortable.slice(0, 3);
  }

  return (
    <Grid item xs={3}>
      <Card>
        <CardContent>
          <Typography variant="h5" component="div">
            {title}
          </Typography>
          <Typography sx={{ fontSize: 18 }}>{category}</Typography>
          <Typography sx={{ fontSize: 13 }}>{url}</Typography>
          <Typography sx={{ fontSize: 13, mt: 1 }}>Top 3 Scores:</Typography>
          {hasScore ? <PrintScores top3scores={top3scores} /> : <React.Fragment></React.Fragment>}
        </CardContent>
        <CardActions>
          <Button size="small">Learn More</Button>
        </CardActions>
      </Card>
    </Grid>
  );
}

const PrintScores = (props) => {
  return (
    <React.Fragment>
      {props.top3scores.map((score, idx) => (
        <Typography key={idx} sx={{ fontSize: 12 }}>
          {score[0]} - {score[1]}
        </Typography>
      ))}
    </React.Fragment>
  );
};
