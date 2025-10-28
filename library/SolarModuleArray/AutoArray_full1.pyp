<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>SolarModuleArray\AutoArray_full.py</Name>
        <Title>Solar Mounting System - 3D Model</Title>
        <Version>1.0.5</Version>
    </Script>

    <Page>
        <Name>Surface</Name>
        <Text>Surface dimensions</Text>

        <Parameter>
            <Name>SurfaceWidth</Name>
            <Text>Width (mm)</Text>
            <Value>8000</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>SurfaceHeight</Name>
            <Text>Height (mm)</Text>
            <Value>6000</Value>
            <ValueType>Length</ValueType>
        </Parameter>
    </Page>

    <Page>
        <Name>Panels</Name>
        <Text>Panel specifications</Text>

        <Parameter>
            <Name>PanelWidth</Name>
            <Text>Panel width (mm)</Text>
            <Value>1700</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>PanelHeight</Name>
            <Text>Panel height (mm)</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>Spacing</Name>
            <Text>Panel spacing (mm)</Text>
            <Value>50</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>PanelThickness</Name>
            <Text>Panel thickness (mm)</Text>
            <Value>35</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>PanelOrientation</Name>
            <Text>Horizontal orientation</Text>
            <Value>0</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>ModuleCount</Name>
            <Text>Total modules</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
            <IsReadOnly>True</IsReadOnly>
        </Parameter>
    </Page>

    <Page>
        <Name>Components</Name>
        <Text>System component dimensions</Text>

        <Parameter>
            <Name>GutterWidth</Name>
            <Text>Gutter width (mm)</Text>
            <Value>80</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>GutterHeight</Name>
            <Text>Gutter height (mm)</Text>
            <Value>40</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>ProfileThickness</Name>
            <Text>Profile thickness (mm)</Text>
            <Value>30</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>RungThickness</Name>
            <Text>Rung thickness (mm)</Text>
            <Value>20</Value>
            <ValueType>Length</ValueType>
        </Parameter>
    </Page>
</Element>
