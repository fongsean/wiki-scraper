import "./App.css";
import { Container } from "@mui/material";
import ThemeProvider from "./ThemeProvider";
import Home from "./components/Home";
import NavBar from "./components/NavBar";
import Simulator from "./components/Simulator";
import Sim from "./components/Sim";
import Dashboard from "./components/Dashboard";

function App(props) {
  const { colorMode } = props;
  return (
    <ThemeProvider mode={colorMode}>
      <div>
        <NavBar></NavBar>
        <Container maxWidth="lg">
          <Home></Home>
          <Simulator></Simulator>
          <Dashboard></Dashboard>
        </Container>
      </div>
    </ThemeProvider>
  );
}

export default App;
