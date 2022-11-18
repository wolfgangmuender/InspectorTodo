package com.tngtech.inspectortodo

import org.junit.Test;
import org.junit.Ignore;

public class IgnoreTest {

    @Test
    @Ignore( "TODO: IT-4: repair test" )
    public void ignored_valid() {}

    @Test
    @Ignore()
    public void ignored_invalid() {}
}
