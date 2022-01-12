import * as React from "react";
import { AppBar, Toolbar, Typography, Container, Button } from "@mui/material";

const NavBar = () => {
  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography variant="h6">Wiki Scraper AI Topic Classifier</Typography>
        </Toolbar>
      </Container>
    </AppBar>
  );
};
export default NavBar;
