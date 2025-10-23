<?xml version="1.0" encoding="utf-8"?>
<Element>
  <Script>
    <Name>SolarModuleArray\SolarModuleArray.py</Name>
    <Title>Solar Module Array</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Array</Name>
    <Text>Array Configuration</Text>
    
    <Parameter>
      <Name>NumRows</Name>
      <Text>Number of rows</Text>
      <Value>3</Value>
      <ValueType>Integer</ValueType>
    </Parameter>
    
    <Parameter>
      <Name>NumCols</Name>
      <Text>Number of columns</Text>
      <Value>4</Value>
      <ValueType>Integer</ValueType>
    </Parameter>
  </Page>
  
  <Page>
    <Name>Module</Name>
    <Text>Module Dimensions</Text>
    
    <Parameter>
      <Name>ModuleWidth</Name>
      <Text>Module width (mm)</Text>
      <Value>1000</Value>
      <ValueType>Length</ValueType>
    </Parameter>
    
    <Parameter>
      <Name>ModuleHeight</Name>
      <Text>Module height (mm)</Text>
      <Value>2000</Value>
      <ValueType>Length</ValueType>
    </Parameter>
    
    <Parameter>
      <Name>ModuleThickness</Name>
      <Text>Module thickness (mm)</Text>
      <Value>35</Value>
      <ValueType>Length</ValueType>
    </Parameter>
    
    <Parameter>
      <Name>RowGap</Name>
      <Text>Gap between rows (mm)</Text>
      <Value>50</Value>
      <ValueType>Length</ValueType>
    </Parameter>
    
    <Parameter>
      <Name>ColGap</Name>
      <Text>Gap between columns (mm)</Text>
      <Value>50</Value>
      <ValueType>Length</ValueType>
    </Parameter>
  </Page>
  
  <Page>
    <Name>Plate</Name>
    <Text>Support Plate</Text>
    
    <Parameter>
      <Name>PlateThickness</Name>
      <Text>Plate thickness (mm)</Text>
      <Value>50</Value>
      <ValueType>Length</ValueType>
    </Parameter>
    
    <Parameter>
      <Name>PlateOffset</Name>
      <Text>Offset from ground (mm)</Text>
      <Value>0</Value>
      <ValueType>Length</ValueType>
    </Parameter>
  </Page>
</Element>
