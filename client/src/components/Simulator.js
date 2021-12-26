import * as React from "react";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import Grid from "@mui/material/Grid";
import InputAdornment from "@mui/material/InputAdornment";
import FormHelperText from "@mui/material/FormHelperText";
import FormControl from "@mui/material/FormControl";

export default function Simulator() {
  return (
    <Grid container spacing={2}>
      <Grid item xs={6}>
        <Autocomplete
          id="combo-box-demo"
          options={top100Films}
          renderInput={(params) => <TextField {...params} label="Movie" />}
        />
      </Grid>

      <Grid item xs={6}>
        <FormControl variant="outlined" fullWidth>
        <TextField
            label="With normal TextField"
            id="outlined-start-adornment"
            InputProps={{
              endAdornment: <InputAdornment position="start">(s)</InputAdornment>,
            }}
            aria-describedby="outlined-duration-helper-text"
            inputProps={{
              "aria-label": "duration",
            }}
            label="Duration"
          />
        </FormControl>
          <FormHelperText id="outlined-duration-helper-text">duration</FormHelperText>
      </Grid>

      {/* <Grid item xs={6}>
        <FormControl variant="outlined">
          <TextField
            label="With normal TextField"
            id="outlined-start-adornment"
            InputProps={{
              endAdornment: <InputAdornment position="start">(s)</InputAdornment>,
            }}
            aria-describedby="outlined-duration-helper-text"
            inputProps={{
              "aria-label": "duration",
            }}
            label="Duration"
          />
          <FormHelperText id="outlined-duration-helper-text">duration</FormHelperText>
        </FormControl>
      </Grid> */}
    </Grid>
  );
}

// Top 100 films as rated by IMDb users. http://www.imdb.com/chart/top
const top100Films = [
  { label: "The Shawshank Redemption", year: 1994 },
  { label: "The Godfather", year: 1972 },
  { label: "The Godfather: Part II", year: 1974 },
  { label: "The Dark Knight", year: 2008 },
  { label: "12 Angry Men", year: 1957 },
  { label: "Schindler's List", year: 1993 },
  { label: "Pulp Fiction", year: 1994 },
];
