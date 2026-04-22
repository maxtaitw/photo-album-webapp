exports.handler = async (event) => {
  const query = event.queryStringParameters && event.queryStringParameters.q;

  return {
    statusCode: 200,
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      query: query || "",
      results: []
    })
  };
};
