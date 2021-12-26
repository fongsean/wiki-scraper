import React, { useState } from "react";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import Input from "@mui/material/Input";
import FilledInput from "@mui/material/FilledInput";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import InputAdornment from "@mui/material/InputAdornment";
import FormHelperText from "@mui/material/FormHelperText";
import FormControl from "@mui/material/FormControl";
import TextField from "@mui/material/TextField";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";

export default function Sim() {
  const [values, setValues] = useState({
    amount: "",
    password: "",
    weight: "",
    weightRange: "",
    showPassword: false,
  });

  return (
    <div>
      <Box sx={{ display: "flex", flexWrap: "wrap" }}>
        <div>
          <FormControl sx={{ m: 1, width: "25ch" }} variant="outlined">
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
        </div>
      </Box>
    </div>
  );
}
