# Tools
# ----------------------------------------------------------------------
PYUIC  := pyside6-uic
PYTHON := python3

# Directories (add more folders here if you need them)
# ----------------------------------------------------------------------
UI_DIRS := . widgets          # <-- search these folders for *.ui

# Find every .ui file in the listed directories
# ----------------------------------------------------------------------
ALL_UI      := $(foreach dir,$(UI_DIRS),$(wildcard $(dir)/*.ui))
# Keep only the base name (without path) for the target name
UI_BASENAMES:= $(notdir $(ALL_UI))

# Destination .py files – same directory as the source .ui
# ----------------------------------------------------------------------
COMPILED_UI := $(patsubst %.ui,%.py,$(ALL_UI))

# Phony targets
# ----------------------------------------------------------------------
.PHONY: all gui clean debug

# Default target
# ----------------------------------------------------------------------
all: gui

# Build every UI file
# ----------------------------------------------------------------------
gui: $(COMPILED_UI)

# Rule:  any_dir/xxx.ui  →  any_dir/xxx.py
# ----------------------------------------------------------------------
%.py: %.ui
	@echo "Compiling UI: $< → $@"
	$(PYUIC) $< -o $@

# Debug – show what will be built
# ----------------------------------------------------------------------
debug:
	@echo "UI directories : $(UI_DIRS)"
	@echo "Found .ui files:"
	@echo "   $(ALL_UI)" | sed 's/^/    /'
	@echo "Will generate .py files:"
	@echo "   $(COMPILED_UI)" | sed 's/^/    /'

# Clean generated Python modules
# ----------------------------------------------------------------------
clean:
	$(RM) $(COMPILED_UI)
