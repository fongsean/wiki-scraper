import React, { useEffect } from 'react'

function Home() {
    const [data, setData] = React.useState(null)
    useEffect(() => {
        fetch("api")
        .then((res) => res.json())
        .then((data) => setData(data.message));

    }, [])
    return (
        <div>
            <p>{!data ? "Loading...": data}</p>
            Wassup
        </div>
    )
}

export default Home
