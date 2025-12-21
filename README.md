# Terminus Logging API

A lightweight, header-only logging facade for C++ applications built on top of Boost.Log. This library provides a simple, consistent interface for structured logging with configurable backends.

## Features

- **Global logging functions**: `tmns::log::trace`, `tmns::log::debug`, `tmns::log::info`, `tmns::log::warn`, `tmns::log::error`, `tmns::log::fatal`
- **Scoped loggers**: `tmns::log::Logger` class for component-specific logging scopes
- **Configurable backends**: Support for console, file, and custom JSON sinks via Boost.Log configuration
- **Header-only design**: Easy integration with minimal build dependencies
- **Thread-safe**: Suitable for multi-threaded applications

## Quick Start

```cpp
#include <terminus/log.hpp>

int main() {
    tmns::log::configure(); // Default console logging

    tmns::log::info("Application started");
    tmns::log::warn("This is a warning");
    tmns::log::error("Something went wrong");

    tmns::log::flush();
    return 0;
}
```

## Installation

### Prerequisites

- C++23 compatible compiler
- Conan package manager
- CMake (for building examples and tests)

### Build Instructions

```bash
# Clone the repository
git clone https://github.com/Terminus-Geospatial/terminus_log
cd terminus_log

# Build and install to Conan cache
conan-build.sh -c

# For first-time builds, you may need to build dependencies from source
conan-build.sh -c --build-missing
```

### Integration with CMake

Add to your `conanfile.txt` or `conanfile.py`:

```python
requires = "terminus_log/1.0.1"
```

Then in your `CMakeLists.txt`:

```cmake
find_package(terminus_log REQUIRED CONFIG)

target_link_libraries(your_target PRIVATE terminus_log::terminus_log)
```


## API Reference

### Log Levels

The library supports standard log levels in order of severity:

- `trace` - Most verbose, typically for debugging
- `debug` - Debugging information
- `info` - General information messages
- `warn` - Warning conditions
- `error` - Error conditions
- `fatal` - Critical errors that may cause termination

### Global Functions

```cpp
// Basic logging
tmns::log::trace("Message with formatting: {}", value);
tmns::log::debug("Debug information");
tmns::log::info("General information");
tmns::log::warn("Warning message");
tmns::log::error("Error occurred");
tmns::log::fatal("Critical error");

// Configuration and control
tmns::log::configure();                    // Default console setup
tmns::log::configure("config_file.ini");   // Custom configuration
tmns::log::flush();                         // Flush all pending logs
tmns::log::shutdown();                      // Clean shutdown
```

### Scoped Logger

```cpp
tmns::log::Logger logger{"my_component"};
logger.info("Component-specific message");
logger.error("Component error: {}", error_code);
```

### Example: simple console logging

```cpp
#include <terminus/log.hpp>

int main()
{
    tmns::log::configure(); // default console sink

    tmns::log::info("Hello, world!");

    tmns::log::Logger logger{"example"};
    logger.debug("Something happened");

    tmns::log::flush();
}
```

## Configuration

### Default Console Logging

```cpp
#include <terminus/log.hpp>

int main() {
    tmns::log::configure(); // Default console sink

    tmns::log::info("Hello, world!");
    tmns::log::Logger logger{"example"};
    logger.debug("Something happened");

    tmns::log::flush();
}
```

### JSON File Logging

For structured logging, create a configuration file (e.g., `logging.conf`):

```ini
[Core]
Filter="%Severity% >= debug"

[Sinks.Console]
Destination=Console
AutoFlush=true

[Sinks.Json]
Destination=JsonFile
FileName="application.log"
TargetFileName="application-%Y%m%d_%H%M%S.log"
Asynchronous=true
RotationSize=10MB

[Formatters.Json]
Format="{\"timestamp\":\"%TimeStamp%\",\"level\":\"%Severity%\",\"message\":\"%Message%\",\"thread\":\"%ThreadID%\"}"
```

Then load it in your code:

```cpp
tmns::log::configure("logging.conf");
```

The custom `JsonFile` sink formats each log entry as JSON with timestamp, log level, message, and thread ID.

### Example: JSON file logging via config file

See `test/component/logging-json.conf` and `TEST_Boost_JSON_File_Logger.cpp` for a complete example. The key bits in the config:

```ini
[Sinks.Json]
Destination=JsonFile
FileName="Json.log"
TargetFileName="Json-%3N.log"
Asynchronous=true
```

This uses the custom `JsonFile` sink registered by `tmns::log::impl::sinks::configure()` and formats each record as JSON using the `tmns::log::impl::format::json` formatter.

## Using terminus-log from CMake

After installing via Conan, you can consume the package from another CMake project using the generated config files:

```cmake
find_package(terminus_log REQUIRED CONFIG)

add_executable(my_app main.cpp)
target_link_libraries(my_app PRIVATE terminus_log::terminus_log)
```

Because `terminus-log` is header-only, linking the target mainly propagates include directories and Boost usage requirements.

## Testing

### Unit Tests

If `with_tests=True` (default) when building with Conan, unit tests are built:

```bash
# Run all unit tests
ctest -V --test-dir build

# Or run from build directory
cd build
ctest -V
```

### Package Integration Test

Test the package integration:

```bash
cd test/package
conan-build.sh -c
./build/example
```

Expected output:

```bash
[2025-12-21 14:31:59.835499] [0x000000020214a0c0] [info]    Hello World!
[2025-12-21 14:31:59.836362] [0x000000020214a0c0] [info]    Terminus Log Build Information:
TERMINUS_LOG_BUILD_DATE: 2025-12-21 14:29:47
TERMINUS_LOG_GIT_COMMIT_HASH:
TERMINUS_LOG_VERSION_MAJOR: 1
TERMINUS_LOG_VERSION_MINOR: 0
TERMINUS_LOG_VERSION_PATCH: 1
TERMINUS_LOG_VERSION_STR: 1.0.1
```

## Troubleshooting

### Common Issues

**Q: No log output appears**
A: Ensure you call `tmns::log::configure()` before logging and `tmns::log::flush()` before program exit.

**Q: Configuration file not found**
A: Use absolute paths or ensure the config file is in the working directory.

**Q: Build fails with Boost errors**
A: Use `--build-missing` flag to build dependencies from source.

**Q: JSON logs not formatted correctly**
A: Verify the `[Formatters.Json]` section in your config file.

### Performance Tips

- Use `tmns::log::flush()` sparingly in production code
- Consider asynchronous logging for high-throughput applications
- Filter messages at compile time using appropriate log levels

## License

Copyright (c) 2024 Terminus LLC. All Rights Reserved.

See LICENSE file for licensing terms.
