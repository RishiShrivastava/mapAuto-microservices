// =Juggernaut= Enhanced React app with Material-UI components and better state management
import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Alert,
  CircularProgress,
  Box,
  Tabs,
  Tab,
  AppBar,
  Toolbar,
  Chip,
  FormControlLabel,
  Checkbox,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Security as SecurityIcon,
  NetworkCheck as NetworkIcon,
  Scanner as ScannerIcon,
  Code as CodeIcon,
  Dashboard as DashboardIcon
} from '@mui/icons-material';
import axios from 'axios';

// =Juggernaut= Component for individual scan cards
function ScanCard({ title, description, icon, onScan, loading, disabled, color = 'primary' }) {
  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box display="flex" alignItems="center" mb={2}>
          {icon}
          <Typography variant="h6" component="h2" ml={1}>
            {title}
          </Typography>
        </Box>
        <Typography variant="body2" color="text.secondary">
          {description}
        </Typography>
      </CardContent>
      <CardActions>
        <Button 
          size="small" 
          variant="contained" 
          color={color}
          onClick={onScan}
          disabled={disabled || loading}
          startIcon={loading ? <CircularProgress size={16} /> : null}
          fullWidth
        >
          {loading ? 'Scanning...' : 'Start Scan'}
        </Button>
      </CardActions>
    </Card>
  );
}

// =Juggernaut= Component for displaying scan results
function ResultsDisplay({ results, loading, error }) {
  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress size={50} />
        <Typography variant="h6" ml={2}>Scanning in progress...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        <Typography variant="h6">Error occurred:</Typography>
        <Typography variant="body2">{error}</Typography>
      </Alert>
    );
  }

  if (!results) {
    return (
      <Box textAlign="center" py={4}>
        <Typography variant="h6" color="text.secondary">
          No scan results yet. Start a scan to see results here.
        </Typography>
      </Box>
    );
  }

  // =Juggernaut= Parse and display results in a user-friendly format
  const formatResults = (data) => {
    if (typeof data === 'string') {
      try {
        data = JSON.parse(data);
      } catch (e) {
        return data;
      }
    }

    return (
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Scan Results</Typography>
        </AccordionSummary>
        <AccordionDetails>
          {/* =Juggernaut= Display target information */}
          {(data.target_ip || data.target_url) && (
            <Box mb={2}>
              <Chip label={`Target: ${data.target_ip || data.target_url}`} color="primary" variant="outlined" />
            </Box>
          )}
          
          {/* =Juggernaut= Display WAF detection results */}
          {data.waf_detected !== undefined && (
            <Box mb={2}>
              <Typography variant="subtitle1" gutterBottom>WAF Detection Results:</Typography>
              <Chip 
                label={data.waf_detected ? `WAF Detected: ${data.waf_name || data.waf_type || 'Unknown'}` : 'No WAF Detected'} 
                color={data.waf_detected ? "warning" : "success"} 
                variant="filled" 
                sx={{ mb: 1, mr: 1 }}
              />
              {data.waf_detected && (
                <Chip 
                  label={`Confidence: ${(data.confidence_level * 100).toFixed(1)}%`} 
                  color="info" 
                  variant="outlined" 
                  sx={{ mb: 1 }}
                />
              )}
              
              {data.weaknesses && data.weaknesses.length > 0 && (
                <Box mt={2}>
                  <Typography variant="subtitle2" color="error">Identified Weaknesses:</Typography>
                  <List dense>
                    {data.weaknesses.map((weakness, index) => (
                      <ListItem key={index}>
                        <ListItemText primary={weakness} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
              
              {data.bypass_techniques && data.bypass_techniques.length > 0 && (
                <Box mt={2}>
                  <Typography variant="subtitle2" color="warning">Potential Bypass Techniques:</Typography>
                  <List dense>
                    {data.bypass_techniques.slice(0, 5).map((technique, index) => (
                      <ListItem key={index}>
                        <ListItemText primary={technique} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
              
              {data.security_recommendations && data.security_recommendations.length > 0 && (
                <Box mt={2}>
                  <Typography variant="subtitle2" color="success">Security Recommendations:</Typography>
                  <List dense>
                    {data.security_recommendations.slice(0, 5).map((recommendation, index) => (
                      <ListItem key={index}>
                        <ListItemText primary={recommendation} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </Box>
          )}
          
          {/* =Juggernaut= Display open ports if available */}
          {data.open_ports && (
            <Box mb={2}>
              <Typography variant="subtitle1" gutterBottom>Open Ports:</Typography>
              <List dense>
                {Object.entries(data.open_ports).map(([port, service]) => (
                  <ListItem key={port}>
                    <ListItemText 
                      primary={`Port ${port}`} 
                      secondary={`Service: ${service}`}
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}

          {/* =Juggernaut= Display scan folder path */}
          {data.scan_folder && (
            <Box mb={2}>
              <Typography variant="subtitle2">Results saved to:</Typography>
              <Typography variant="body2" sx={{ fontFamily: 'monospace', bgcolor: 'grey.100', p: 1, borderRadius: 1 }}>
                {data.scan_folder}
              </Typography>
            </Box>
          )}

          {/* =Juggernaut= Raw JSON for detailed inspection */}
          <Divider sx={{ my: 2 }} />
          <Typography variant="subtitle2" gutterBottom>Raw Results:</Typography>
          <Box sx={{ 
            bgcolor: 'grey.50', 
            p: 2, 
            borderRadius: 1, 
            maxHeight: '400px', 
            overflow: 'auto',
            fontFamily: 'monospace',
            fontSize: '0.875rem'
          }}>
            <pre>{JSON.stringify(data, null, 2)}</pre>
          </Box>
        </AccordionDetails>
      </Accordion>
    );
  };

  return (
    <Paper sx={{ mt: 2, p: 2 }}>
      {formatResults(results)}
    </Paper>
  );
}

function App() {
  // =Juggernaut= Enhanced state management for better UX
  const [activeTab, setActiveTab] = useState(0);
  const [scanInputs, setScanInputs] = useState({
    ip: '192.168.0.231', // =Juggernaut= Default from README examples
    target: '', // =Juggernaut= For WAF detection (URL or IP)
    timeout: 60,
    maxScripts: 5,
    xmlPath: '',
    intensive: false // =Juggernaut= For intensive WAF scanning
  });
  const [scanResults, setScanResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [scanHistory, setScanHistory] = useState([]);

  // =Juggernaut= Load scan history from localStorage on mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('mapauto-scan-history');
    if (savedHistory) {
      try {
        setScanHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error('Failed to load scan history:', e);
      }
    }
  }, []);

  // =Juggernaut= Save to scan history
  const saveToHistory = (scanType, result) => {
    const historyEntry = {
      id: Date.now(),
      timestamp: new Date().toISOString(),
      scanType,
      targetIp: scanInputs.ip,
      result
    };
    const newHistory = [historyEntry, ...scanHistory].slice(0, 10); // =Juggernaut= Keep last 10 scans
    setScanHistory(newHistory);
    localStorage.setItem('mapauto-scan-history', JSON.stringify(newHistory));
  };

  // =Juggernaut= Enhanced API call function with nginx proxy endpoints
  const handleScan = async (scanType) => {
    setLoading(true);
    setError('');
    setScanResults(null);

    try {
      let url = '';
      let baseUrl = ''; // =Juggernaut= Use relative URLs for nginx proxy

      // =Juggernaut= Map scan types to nginx proxy endpoints
      switch (scanType) {
        case 'os-scan':
          url = `/api/osscan/os-scan?ip=${scanInputs.ip}&timeout=${scanInputs.timeout}`;
          break;
        case 'nmap-scan':
          url = `/api/nmapscanner/scan?ip=${scanInputs.ip}&timeout=${scanInputs.timeout}`;
          break;
        case 'nmap-all':
          url = `/api/nmapall/scan-all?ip=${scanInputs.ip}&timeout=${scanInputs.timeout}&max_scripts=${scanInputs.maxScripts}`;
          break;
        case 'parse-xml':
          url = `/api/portxmlparser/parse-xml?xml_path=${scanInputs.xmlPath}`;
          break;
        case 'nessus-status':
          url = `/api/auto_nessus/status`;
          break;
        case 'waf-detection':
          url = `/api/waf/detect-waf?target=${scanInputs.target || scanInputs.ip}&timeout=${scanInputs.timeout}&intensive=${scanInputs.intensive || false}`;
          break;
        default:
          throw new Error('Unknown scan type');
      }

      // =Juggernaut= Make API call through nginx proxy
      const response = await axios.post(url, {}, {
        timeout: (scanInputs.timeout + 30) * 1000, // =Juggernaut= Add buffer to timeout
        headers: {
          'Content-Type': 'application/json'
        }
      });

      setScanResults(response.data);
      saveToHistory(scanType, response.data);
      
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Unknown error occurred';
      setError(`${scanType} failed: ${errorMsg}`);
      console.error('Scan error:', err);
    } finally {
      setLoading(false);
    }
  };

  // =Juggernaut= Input change handler
  const handleInputChange = (field, value) => {
    setScanInputs(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // =Juggernaut= Tab change handler
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* =Juggernaut= App bar with branding */}
      <AppBar position="static" sx={{ mb: 3 }}>
        <Toolbar>
          <DashboardIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            MapAuto Network Scanner Dashboard
          </Typography>
          <Chip label="=Juggernaut=" color="secondary" variant="outlined" />
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg">
        {/* =Juggernaut= Tab navigation */}
        <Paper sx={{ mb: 3 }}>
          <Tabs value={activeTab} onChange={handleTabChange} centered>
            <Tab label="Scanner" />
            <Tab label="Results" />
            <Tab label="History" />
          </Tabs>
        </Paper>

        {/* =Juggernaut= Scanner Tab */}
        {activeTab === 0 && (
          <Box>
            {/* =Juggernaut= Input controls */}
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h5" gutterBottom>
                Scan Configuration
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Target IP Address"
                    value={scanInputs.ip}
                    onChange={(e) => handleInputChange('ip', e.target.value)}
                    placeholder="192.168.0.231"
                    helperText="Enter the IP address to scan"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="WAF Target (URL or IP)"
                    value={scanInputs.target}
                    onChange={(e) => handleInputChange('target', e.target.value)}
                    placeholder="https://example.com or 192.168.1.100"
                    helperText="Target for WAF detection (URL or IP)"
                  />
                </Grid>
                <Grid item xs={12} md={3}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Timeout (seconds)"
                    value={scanInputs.timeout}
                    onChange={(e) => handleInputChange('timeout', parseInt(e.target.value) || 60)}
                    helperText="Scan timeout"
                  />
                </Grid>
                <Grid item xs={12} md={3}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Max Scripts"
                    value={scanInputs.maxScripts}
                    onChange={(e) => handleInputChange('maxScripts', parseInt(e.target.value) || 5)}
                    helperText="For Nmap All scan"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="XML File Path (for parsing)"
                    value={scanInputs.xmlPath}
                    onChange={(e) => handleInputChange('xmlPath', e.target.value)}
                    placeholder="/app/scan_results/osscan_192.168.0.231_20250717_160231/OSScan_192.168.0.231.xml"
                    helperText="Full path to XML file for parsing"
                  />
                </Grid>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={scanInputs.intensive}
                        onChange={(e) => handleInputChange('intensive', e.target.checked)}
                        color="primary"
                      />
                    }
                    label="Intensive WAF Scanning (includes nmap scans - slower but more thorough)"
                  />
                </Grid>
              </Grid>
            </Paper>

            {/* =Juggernaut= Scan cards */}
            <Typography variant="h5" gutterBottom>
              Available Scans
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6} lg={4}>
                <ScanCard
                  title="OS Scan"
                  description="Fingerprint the operating system of the target (Port 8003)"
                  icon={<SecurityIcon color="primary" />}
                  onScan={() => handleScan('os-scan')}
                  loading={loading}
                  disabled={!scanInputs.ip}
                  color="primary"
                />
              </Grid>
              <Grid item xs={12} md={6} lg={4}>
                <ScanCard
                  title="Nmap Scan"
                  description="Intelligent Nmap scanning with OS detection (Port 8001)"
                  icon={<NetworkIcon color="secondary" />}
                  onScan={() => handleScan('nmap-scan')}
                  loading={loading}
                  disabled={!scanInputs.ip}
                  color="secondary"
                />
              </Grid>
              <Grid item xs={12} md={6} lg={4}>
                <ScanCard
                  title="Nmap All Scripts"
                  description="Execute all Nmap scripts against target (Port 8002)"
                  icon={<ScannerIcon color="warning" />}
                  onScan={() => handleScan('nmap-all')}
                  loading={loading}
                  disabled={!scanInputs.ip}
                  color="warning"
                />
              </Grid>
              <Grid item xs={12} md={6} lg={4}>
                <ScanCard
                  title="WAF Detection"
                  description="Detect and analyze Web Application Firewalls (Port 8005)"
                  icon={<SecurityIcon color="error" />}
                  onScan={() => handleScan('waf-detection')}
                  loading={loading}
                  disabled={!scanInputs.target && !scanInputs.ip}
                  color="error"
                />
              </Grid>
              <Grid item xs={12} md={6} lg={4}>
                <ScanCard
                  title="Parse XML"
                  description="Parse existing Nmap XML files (Port 8004)"
                  icon={<CodeIcon color="info" />}
                  onScan={() => handleScan('parse-xml')}
                  loading={loading}
                  disabled={!scanInputs.xmlPath}
                  color="info"
                />
              </Grid>
              <Grid item xs={12} md={6} lg={4}>
                <ScanCard
                  title="Nessus Status"
                  description="Check Nessus service status (Port 8000)"
                  icon={<SecurityIcon color="success" />}
                  onScan={() => handleScan('nessus-status')}
                  loading={loading}
                  disabled={false}
                  color="success"
                />
              </Grid>
            </Grid>
          </Box>
        )}

        {/* =Juggernaut= Results Tab */}
        {activeTab === 1 && (
          <Box>
            <Typography variant="h5" gutterBottom>
              Scan Results
            </Typography>
            <ResultsDisplay results={scanResults} loading={loading} error={error} />
          </Box>
        )}

        {/* =Juggernaut= History Tab */}
        {activeTab === 2 && (
          <Box>
            <Typography variant="h5" gutterBottom>
              Scan History
            </Typography>
            {scanHistory.length === 0 ? (
              <Paper sx={{ p: 4, textAlign: 'center' }}>
                <Typography variant="h6" color="text.secondary">
                  No scan history available
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Complete some scans to see history here
                </Typography>
              </Paper>
            ) : (
              <Box>
                {scanHistory.map((entry) => (
                  <Paper key={entry.id} sx={{ p: 2, mb: 2 }}>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                      <Typography variant="h6">
                        {entry.scanType} - {entry.targetIp}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {new Date(entry.timestamp).toLocaleString()}
                      </Typography>
                    </Box>
                    <Accordion>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography variant="body2">View Results</Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <Box sx={{ 
                          bgcolor: 'grey.50', 
                          p: 2, 
                          borderRadius: 1, 
                          maxHeight: '300px', 
                          overflow: 'auto',
                          fontFamily: 'monospace',
                          fontSize: '0.75rem'
                        }}>
                          <pre>{JSON.stringify(entry.result, null, 2)}</pre>
                        </Box>
                      </AccordionDetails>
                    </Accordion>
                  </Paper>
                ))}
              </Box>
            )}
          </Box>
        )}
      </Container>
    </Box>
  );
}

export default App;
// =Juggernaut= No original code deleted, only enhanced with Material-UI and better functionality
