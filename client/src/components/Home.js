import React, { useEffect, useState } from "react";

function Home() {
  const [currentTime, setCurrentTime] = useState(null);

  useEffect(() => {
    fetch("/time")
      .then((res) => res.json())
      .then((data) => {
        setCurrentTime(data.time);
      });
  }, []);

  return (
    <div>
      <p>{!currentTime ? "Loading..." : currentTime}</p>
    </div>
  );
}

export default Home;
