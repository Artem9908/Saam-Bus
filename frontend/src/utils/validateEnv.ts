export const validateEnv = () => {
  const requiredVars = ['REACT_APP_API_URL'];
  
  for (const varName of requiredVars) {
    if (!process.env[varName]) {
      throw new Error(`Missing required environment variable: ${varName}`);
    }
  }
};

export default validateEnv; 