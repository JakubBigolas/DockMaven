function toolHelpOptionPrint {
  local width="16"
  [[ -n "$3" ]] && width="$3"
   printf " ${C_BLUE}%-${width}s ${C_RESET}%s\n" "$1" "$2"
}