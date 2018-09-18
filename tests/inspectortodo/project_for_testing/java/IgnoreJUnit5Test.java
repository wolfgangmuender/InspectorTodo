// Copyright 2018 TNG Technology Consulting GmbH, Unterfoehring, Germany
// Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

package com.tngtech.inspectortodo

import org.junit.Test;
import org.junit.Ignore;

public class IgnoreTest {

    @Test
    @Disabled()
    public void disabled_invalid() {}
}
