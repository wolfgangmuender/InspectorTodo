package com.tngtech.inspectortodo

import org.junit.Test;
import org.junit.Ignore;

public class IgnoreTest {

    @Test
    @Disabled()
    public void disabled_invalid() {}
}
