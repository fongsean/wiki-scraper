import "./App.css";
import { Container } from "@mui/material";
import ThemeProvider from "./ThemeProvider";
import NavBar from "./components/NavBar";
import Dashboard from "./components/Dashboard";

function App(props) {
  const { colorMode } = props;
  return (
    <ThemeProvider mode={colorMode}>
      <div>
        <NavBar></NavBar>
        <Container maxWidth="xl">
          <Dashboard></Dashboard>
        </Container>
      </div>
    </ThemeProvider>
  );
}

export default App;
