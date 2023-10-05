CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wextra -Wpedantic -Werror -DDEBUG_LEVEL=92
LDFLAGS :=

SRCS    := $(sort $(wildcard *.cpp))
OBJECTS := $(patsubst %.cpp,%.o,$(SRCS))
TARGETS := main

MAINSRCS    := $(shell egrep 'int main' $(SRCS) | awk -F: '{print $$1;}' | uniq)
COMMON_SRCS := $(sort $(SRCS))
COMMON_SRCS := $(filter-out $(MAINSRCS),$(COMMON_SRCS))
COMMON_OBJECTS := $(patsubst %.cpp,%.o,$(COMMON_SRCS))

all: $(TARGETS)

main: main.o $(COMMON_OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)


######################################
# automatic dependency generation
#
DEPDIR := .d
$(shell mkdir -p $(DEPDIR) >/dev/null)
DEPFLAGS = -MT $@ -MMD -MP -MF $(DEPDIR)/$*.Td

COMPILE.cc = $(CXX) $(DEPFLAGS) $(CXXFLAGS) $(CPPFLAGS) $(TARGET_ARCH) -c
POSTCOMPILE = @mv -f $(DEPDIR)/$*.Td $(DEPDIR)/$*.d && touch $@

%.o : %.cpp
%.o : %.cpp $(DEPDIR)/%.d
	$(COMPILE.cc) $(OUTPUT_OPTION) $<
	$(POSTCOMPILE)

$(DEPDIR)/%.d: ;
.PRECIOUS: $(DEPDIR)/%.d

include $(wildcard $(patsubst %,$(DEPDIR)/%.d,$(basename $(SRCS))))
#
#
######################################

######################################
#
#
clean:
	-rm -f $(TARGETS)
	-rm -f *.o
	-rm -f *~
	-rm -rf $(DEPDIR)
#
#
######################################
