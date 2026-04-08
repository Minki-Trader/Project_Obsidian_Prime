#property strict
#property version   "1.000"
#property description "Project Obsidian Prime Stage 1 shadow EA shell"

#include <Trade/Trade.mqh>

#define OP_FEATURE_COUNT 58
#define OP_OUTPUT_COUNT 3

enum ENUM_OP_FEATURE_MODE
{
   OP_FEATURE_MODE_ZERO_SMOKE = 0,
   OP_FEATURE_MODE_PRICE_CORE_PARTIAL = 1,
   OP_FEATURE_MODE_SKIP_UNIMPLEMENTED = 2
};

#define OP_IDX_LOG_RETURN_1                0
#define OP_IDX_LOG_RETURN_3                1
#define OP_IDX_HL_RANGE                    2
#define OP_IDX_CLOSE_OPEN_RATIO            3
#define OP_IDX_GAP_PERCENT                 4
#define OP_IDX_CLOSE_PREV_CLOSE_RATIO      5
#define OP_IDX_RETURN_ZSCORE_20            6
#define OP_IDX_HL_ZSCORE_50                7
#define OP_IDX_ROC_12                      24
#define OP_IDX_HISTORICAL_VOL_20           32
#define OP_IDX_HISTORICAL_VOL_5_OVER_20    33
#define OP_PRICE_CORE_READY_COUNT          11
#define OP_BARS_PER_YEAR_5M                72576.0
#define OP_TOP3_EQUAL_WEIGHT               0.333333333333

input string               InpOnnxModelPath        = "Project_Obsidian_Prime\\obsidian_prime_stage01d.onnx";
input bool                 InpOnnxUseCommonFiles   = false;
input bool                 InpUseRuntimeConfig     = false;
input string               InpRuntimeConfigPath    = "Project_Obsidian_Prime\\runtime\\default\\mt5_runtime_config.txt";
input bool                 InpRuntimeConfigUseCommonFiles = true;
input bool                 InpUseCpuOnly           = true;
input bool                 InpDumpModelIo          = true;
input bool                 InpRunSmokeOnInit       = true;
input ENUM_OP_FEATURE_MODE InpFeatureMode          = OP_FEATURE_MODE_ZERO_SMOKE;
input int                  InpWarmupBars           = 300;
input double               InpShortThreshold       = 0.333333;
input double               InpLongThreshold        = 0.333333;
input double               InpMinMargin            = 0.0;
input double               InpFixedLot             = 0.1;
input bool                 InpEnableTrading        = false;
input long                 InpMagicNumber          = 26032901;
input int                  InpTradeDeviationPoints = 100;
input bool                 InpAllowPartialInference = false;
input bool                 InpWriteCsvLog          = true;
input bool                 InpLogUseCommonFiles    = false;
input string               InpCsvLogPath           = "Project_Obsidian_Prime\\obsidian_prime_stage1_shadow_log.csv";
input bool                 InpWriteTradeLedger     = true;
input bool                 InpTradeLedgerUseCommonFiles = false;
input string               InpTradeLedgerPath      = "Project_Obsidian_Prime\\obsidian_prime_stage1_trade_ledger.csv";
input bool                 InpEnableGovernance     = false;
input bool                 InpGovernanceBlockNewEntries = false;
input int                  InpGovernanceWindowBars = 144;
input int                  InpGovernanceMinSamples = 48;
input double               InpGovernanceMaxOperationalSkipRate = 0.15;
input double               InpGovernanceMaxExternalSkipRate = 0.05;
input double               InpGovernanceMaxFeatureSkipRate = 0.08;
input int                  InpGovernanceMaxConsecutiveOperationalSkips = 4;
input double               InpGovernanceMaxArgmaxClassShare = 0.90;
input double               InpGovernanceMaxExtremeConfidenceRate = 0.50;
input double               InpGovernanceExtremeConfidenceThreshold = 0.97;
input double               InpGovernanceMinNormalizedEntropy = 0.20;
input bool                 InpWriteGovernanceLog   = true;
input bool                 InpGovernanceLogUseCommonFiles = false;
input string               InpGovernanceLogPath    = "Project_Obsidian_Prime\\obsidian_prime_stage1_governance_log.csv";
input bool                 InpVerboseLog           = true;

datetime g_last_chart_bar_open = 0;
bool     g_shadow_ready        = false;
bool     g_log_header_written  = false;
bool     g_trade_ledger_header_written = false;
bool     g_governance_log_header_written = false;
long     g_onnx_handle         = INVALID_HANDLE;
uint     g_onnx_run_flags      = 0;
int      g_handle_ema9         = INVALID_HANDLE;
int      g_handle_ema20        = INVALID_HANDLE;
int      g_handle_ema50        = INVALID_HANDLE;
int      g_handle_ema200       = INVALID_HANDLE;
int      g_handle_sma50        = INVALID_HANDLE;
int      g_handle_sma200       = INVALID_HANDLE;
int      g_handle_rsi14        = INVALID_HANDLE;
int      g_handle_rsi50        = INVALID_HANDLE;
int      g_handle_atr14        = INVALID_HANDLE;
int      g_handle_atr20        = INVALID_HANDLE;
int      g_handle_atr50        = INVALID_HANDLE;
int      g_handle_bands20      = INVALID_HANDLE;
int      g_handle_adx14        = INVALID_HANDLE;
int      g_handle_stoch14      = INVALID_HANDLE;
ulong    g_input_shape[];
ulong    g_output_shape[];
float    g_input_tensor[];
float    g_output_tensor[];
CTrade   g_trade;
int      g_effective_feature_count = OP_FEATURE_COUNT;
string   g_effective_feature_names[];
string   g_effective_onnx_model_path = "";
bool     g_effective_onnx_use_common_files = false;
double   g_effective_short_threshold = 0.0;
double   g_effective_long_threshold = 0.0;
double   g_effective_min_margin = 0.0;
double   g_effective_min_probability_diff = 0.0;
string   g_effective_sizing_mode = "fixed_lot";
double   g_effective_fixed_lot = 0.1;
double   g_effective_risk_pct = 0.0;
string   g_effective_capital_base = "balance";
double   g_effective_monday_risk_pct_mult = 1.0;
double   g_effective_ny_postcash_risk_pct_mult = 1.0;
double   g_effective_monday_long_risk_pct_mult = 1.0;
double   g_effective_monday_short_risk_pct_mult = 1.0;
int      g_effective_ny_postcash_hold_cap_bars = 0;
int      g_effective_ny_clock_taper_start_minute = -1;
int      g_effective_ny_clock_taper_mid_minute = -1;
int      g_effective_ny_clock_taper_late_minute = -1;
double   g_effective_ny_clock_taper_start_mult = 1.0;
double   g_effective_ny_clock_taper_mid_mult = 1.0;
double   g_effective_ny_clock_taper_late_mult = 1.0;
string   g_effective_stop_model = "";
string   g_effective_stop_execution_mode = "ea_managed";
string   g_effective_stop_policy = "fixed";
int      g_effective_stop_atr_period = 14;
double   g_effective_stop_atr_mult = 0.0;
double   g_effective_stop_long_atr_mult = 0.0;
double   g_effective_stop_short_atr_mult = 0.0;
double   g_effective_stop_low_vol_threshold = 0.0;
double   g_effective_stop_high_vol_threshold = 0.0;
double   g_effective_stop_low_atr_mult = 0.0;
double   g_effective_stop_mid_atr_mult = 0.0;
double   g_effective_stop_high_atr_mult = 0.0;
string   g_effective_external_alignment_mode = "exact";
string   g_effective_external_relaxed_scope = "none";
int      g_effective_external_max_stale_bars = 0;
int      g_effective_max_hold_bars = 3;
int      g_effective_max_concurrent_positions = 1;
bool     g_effective_time_exit_enabled = true;
bool     g_effective_flat_exit_enabled = false;
double   g_effective_flat_exit_min_probability = 0.0;
int      g_effective_flat_exit_min_hold_bars = 1;
bool     g_effective_threshold_rule_enabled = true;
bool     g_effective_margin_rule_enabled = false;
bool     g_effective_prob_diff_rule_enabled = false;
string   g_effective_experiment_id = "";
string   g_effective_bundle_version = "";
string   g_effective_logic_family = "";
string   g_effective_feature_fingerprint = "";
string   g_effective_exit_rule_types[];
bool     g_effective_exit_rule_enabled[];
int      g_effective_exit_rule_max_hold_bars[];
double   g_effective_exit_rule_min_flat_probability[];
int      g_effective_exit_rule_min_hold_bars[];
double   g_effective_exit_rule_trigger_points[];
double   g_effective_exit_rule_offset_points[];
double   g_effective_exit_rule_distance_points[];
double   g_effective_exit_rule_close_fraction[];
bool     g_runtime_config_loaded = false;
datetime g_entry_block_bar_time = 0;
bool     g_managed_trade_active = false;
ulong    g_managed_position_ticket = 0;
long     g_managed_position_identifier = 0;
long     g_managed_position_type = -1;
datetime g_managed_entry_time_server = 0;
datetime g_managed_entry_bar_time_server = 0;
ulong    g_managed_entry_deal_ticket = 0;
double   g_managed_entry_price = 0.0;
double   g_managed_entry_volume = 0.0;
double   g_managed_max_floating_profit = 0.0;
double   g_managed_min_floating_profit = 0.0;
int      g_managed_entry_decision = 0;
string   g_managed_entry_decision_text = "";
string   g_managed_sizing_mode = "";
string   g_managed_stop_policy = "";
string   g_managed_risk_context = "";
double   g_managed_initial_stop_price = 0.0;
double   g_managed_initial_stop_distance_price = 0.0;
double   g_managed_initial_risk_amount = 0.0;
double   g_managed_risk_pct_multiplier = 1.0;
double   g_managed_stop_atr_mult_applied = 0.0;
double   g_managed_peak_favorable_points = 0.0;
bool     g_managed_exit_rule_triggered[];
double   g_last_trade_fill_price = 0.0;
bool     g_external_alignment_fallback_used = false;
int      g_external_alignment_fallback_count = 0;
string   g_external_alignment_fallback_details = "";
int      g_governance_skip_category_window[];
int      g_governance_inference_ready_window[];
int      g_governance_argmax_window[];
int      g_governance_extreme_confidence_window[];
double   g_governance_entropy_window[];
int      g_governance_signal_window[];
int      g_governance_overlay_window[];
int      g_governance_window_slot = 0;
int      g_governance_window_count = 0;
string   g_governance_state = "DISABLED";
string   g_governance_reason = "GOVERNANCE_DISABLED";
bool     g_governance_entry_blocked = false;
int      g_governance_window_samples = 0;
int      g_governance_inference_samples = 0;
int      g_governance_signal_samples = 0;
int      g_governance_consecutive_operational_skips = 0;
double   g_governance_operational_skip_rate = 0.0;
double   g_governance_external_skip_rate = 0.0;
double   g_governance_feature_skip_rate = 0.0;
double   g_governance_warmup_skip_rate = 0.0;
double   g_governance_max_argmax_class_share = 0.0;
double   g_governance_extreme_confidence_rate = 0.0;
double   g_governance_avg_signal_entropy = EMPTY_VALUE;
double   g_governance_risk_overlay_rate = EMPTY_VALUE;
string   g_governance_current_skip_category = "NONE";
string   g_governance_current_argmax_class = "";
double   g_governance_current_signal_entropy = EMPTY_VALUE;
double   g_governance_current_max_probability = EMPTY_VALUE;
bool     g_governance_current_extreme_confidence = false;
string   g_governance_current_risk_context = "BASE";
double   g_governance_current_risk_pct_multiplier = 1.0;

enum ENUM_OP_GOV_SKIP_CATEGORY
{
   OP_GOV_SKIP_NONE = 0,
   OP_GOV_SKIP_WARMUP = 1,
   OP_GOV_SKIP_EXTERNAL = 2,
   OP_GOV_SKIP_FEATURE = 3,
   OP_GOV_SKIP_RUNTIME = 4,
   OP_GOV_SKIP_OTHER = 5
};

string TrimText(const string value)
{
   string out = value;
   StringTrimLeft(out);
   StringTrimRight(out);
   return out;
}

void ResetExternalAlignmentTelemetry()
{
   g_external_alignment_fallback_used = false;
   g_external_alignment_fallback_count = 0;
   g_external_alignment_fallback_details = "";
}

bool SameUtcCalendarDate(const datetime left_value, const datetime right_value)
{
   MqlDateTime left_struct;
   MqlDateTime right_struct;
   ZeroMemory(left_struct);
   ZeroMemory(right_struct);
   if(!TimeToStruct(left_value, left_struct))
      return false;
   if(!TimeToStruct(right_value, right_struct))
      return false;
   return left_struct.year == right_struct.year &&
      left_struct.mon == right_struct.mon &&
      left_struct.day == right_struct.day;
}

bool IsMacroExternalSymbol(const string symbol)
{
   return symbol == "VIX" || symbol == "US10YR" || symbol == "USDX";
}

bool AllowExternalStaleFallback(const string symbol)
{
   if(g_effective_external_alignment_mode != "stale_closed_bar")
      return false;
   if(g_effective_external_max_stale_bars <= 0)
      return false;
   if(g_effective_external_relaxed_scope == "all")
      return true;
   if(g_effective_external_relaxed_scope == "macro_only")
      return IsMacroExternalSymbol(symbol);
   if(g_effective_external_relaxed_scope == "breadth_only")
      return !IsMacroExternalSymbol(symbol);
   return false;
}

void RecordExternalAlignmentFallback(const string symbol, const int stale_bars)
{
   g_external_alignment_fallback_used = true;
   g_external_alignment_fallback_count++;
   if(StringLen(g_external_alignment_fallback_details) > 0)
      g_external_alignment_fallback_details += "|";
   g_external_alignment_fallback_details += symbol + ":" + (string)stale_bars;
}

bool ParseBoolText(const string value, bool &result)
{
   string normalized = TrimText(value);
   StringToLower(normalized);
   if(normalized == "true" || normalized == "1" || normalized == "yes")
   {
      result = true;
      return true;
   }
   if(normalized == "false" || normalized == "0" || normalized == "no")
   {
      result = false;
      return true;
   }
   return false;
}

double NormalizeVolumeForSymbol(const double raw_volume)
{
   if(raw_volume <= 0.0)
      return 0.0;

   const double min_volume = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   const double max_volume = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   const double volume_step = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   if(min_volume <= 0.0 || max_volume <= 0.0 || volume_step <= 0.0)
      return 0.0;

   const double stepped_volume = MathFloor((raw_volume / volume_step) + 1e-9) * volume_step;
   if(stepped_volume < min_volume)
      return 0.0;

   double normalized_volume = stepped_volume;
   if(normalized_volume > max_volume)
      normalized_volume = max_volume;
   return NormalizeDouble(normalized_volume, 8);
}

double NormalizePriceForSymbol(const double raw_price)
{
   const int digits = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
   if(digits < 0)
      return raw_price;
   return NormalizeDouble(raw_price, digits);
}

double ResolveRiskCapitalBase()
{
   if(g_effective_capital_base == "equity")
      return AccountInfoDouble(ACCOUNT_EQUITY);
   return AccountInfoDouble(ACCOUNT_BALANCE);
}

void AppendRiskContextTag(string &tags, const string tag)
{
   if(StringLen(tag) <= 0)
      return;
   if(StringLen(tags) > 0)
      tags += "|";
   tags += tag;
}

double ResolveDynamicRiskPctMultiplier(const int decision, const datetime bar_time_server, string &risk_context)
{
   risk_context = "BASE";
   double multiplier = 1.0;
   string tags = "";

   if(bar_time_server <= 0)
      return multiplier;

   const datetime ny_time = ConvertUtcToNewYork(bar_time_server);
   MqlDateTime ny_struct;
   ZeroMemory(ny_struct);
   if(!TimeToStruct(ny_time, ny_struct))
      return multiplier;

   if(g_effective_monday_risk_pct_mult > 0.0 && MathAbs(g_effective_monday_risk_pct_mult - 1.0) > 0.0000001 && ny_struct.day_of_week == 1)
   {
      multiplier *= g_effective_monday_risk_pct_mult;
      AppendRiskContextTag(tags, "MONDAY");
   }

   if(ny_struct.day_of_week == 1)
   {
      if(decision > 0 && g_effective_monday_long_risk_pct_mult > 0.0 && MathAbs(g_effective_monday_long_risk_pct_mult - 1.0) > 0.0000001)
      {
         multiplier *= g_effective_monday_long_risk_pct_mult;
         AppendRiskContextTag(tags, "MONDAY_LONG");
      }
      if(decision < 0 && g_effective_monday_short_risk_pct_mult > 0.0 && MathAbs(g_effective_monday_short_risk_pct_mult - 1.0) > 0.0000001)
      {
         multiplier *= g_effective_monday_short_risk_pct_mult;
         AppendRiskContextTag(tags, "MONDAY_SHORT");
      }
   }

   const int minutes_of_day = (ny_struct.hour * 60) + ny_struct.min;
   if(g_effective_ny_clock_taper_start_minute >= 0)
   {
      double taper_mult = 1.0;
      string taper_tag = "";
      if(g_effective_ny_clock_taper_late_minute >= 0 && minutes_of_day >= g_effective_ny_clock_taper_late_minute)
      {
         taper_mult = g_effective_ny_clock_taper_late_mult;
         taper_tag = "CLOCK_TAPER_LATE";
      }
      else if(g_effective_ny_clock_taper_mid_minute >= 0 && minutes_of_day >= g_effective_ny_clock_taper_mid_minute)
      {
         taper_mult = g_effective_ny_clock_taper_mid_mult;
         taper_tag = "CLOCK_TAPER_MID";
      }
      else if(minutes_of_day >= g_effective_ny_clock_taper_start_minute)
      {
         taper_mult = g_effective_ny_clock_taper_start_mult;
         taper_tag = "CLOCK_TAPER_EARLY";
      }

      if(taper_mult > 0.0 && MathAbs(taper_mult - 1.0) > 0.0000001)
      {
         multiplier *= taper_mult;
         AppendRiskContextTag(tags, taper_tag);
      }
   }

   if(g_effective_ny_postcash_risk_pct_mult > 0.0 && MathAbs(g_effective_ny_postcash_risk_pct_mult - 1.0) > 0.0000001 && minutes_of_day >= (16 * 60))
   {
      multiplier *= g_effective_ny_postcash_risk_pct_mult;
      AppendRiskContextTag(tags, "NY_POSTCASH");
   }

   if(StringLen(tags) > 0)
      risk_context = tags;
   return multiplier;
}

int ResolveDynamicMaxHoldBars(const datetime bar_time_server, string &hold_context)
{
   hold_context = "BASE";
   int resolved_hold_bars = g_effective_max_hold_bars;
   if(bar_time_server <= 0 || resolved_hold_bars <= 0)
      return resolved_hold_bars;

   const datetime ny_time = ConvertUtcToNewYork(bar_time_server);
   MqlDateTime ny_struct;
   ZeroMemory(ny_struct);
   if(!TimeToStruct(ny_time, ny_struct))
      return resolved_hold_bars;

   const int minutes_of_day = (ny_struct.hour * 60) + ny_struct.min;
   if(g_effective_ny_postcash_hold_cap_bars > 0 && minutes_of_day >= (16 * 60) && g_effective_ny_postcash_hold_cap_bars < resolved_hold_bars)
   {
      resolved_hold_bars = g_effective_ny_postcash_hold_cap_bars;
      hold_context = "NY_POSTCASH";
   }
   return resolved_hold_bars;
}

bool IsSupportedAtrPeriod(const int period)
{
   return (period == 14 || period == 20 || period == 50);
}

int ResolveAtrHandleByPeriod(const int period)
{
   if(period == 14)
      return g_handle_atr14;
   if(period == 20)
      return g_handle_atr20;
   if(period == 50)
      return g_handle_atr50;
   return INVALID_HANDLE;
}

bool ComputeAtrStopDistancePrice(const int atr_period, const double atr_mult, double &distance_price, string &reason)
{
   distance_price = 0.0;
   const int atr_handle = ResolveAtrHandleByPeriod(atr_period);
   if(atr_handle == INVALID_HANDLE)
   {
      reason = StringFormat("STOP_ATR_HANDLE_UNSUPPORTED_%d", atr_period);
      return false;
   }

   double atr_values[];
   if(!CopyIndicatorBufferWindow(atr_handle, 0, 1, 1, atr_values, StringFormat("ATR%d", atr_period), reason))
      return false;

   distance_price = atr_values[0] * atr_mult;
   if(!IsUsableValue(distance_price) || distance_price <= 0.0)
   {
      reason = "STOP_DISTANCE_INVALID";
      return false;
   }
   return true;
}

bool ResolveEffectiveStopAtrMult(const int decision, double &atr_mult, string &policy_context)
{
   atr_mult = 0.0;
   policy_context = "";

   if(g_effective_stop_policy == "fixed")
   {
      atr_mult = g_effective_stop_atr_mult;
      policy_context = "FIXED";
   }
   else if(g_effective_stop_policy == "direction_split")
   {
      atr_mult = (decision > 0) ? g_effective_stop_long_atr_mult : g_effective_stop_short_atr_mult;
      policy_context = (decision > 0) ? "DIR_LONG" : "DIR_SHORT";
   }
   else if(g_effective_stop_policy == "regime_bucket")
   {
      double atr14_values[];
      double atr50_values[];
      string reason = "";
      if(!CopyIndicatorBufferWindow(g_handle_atr14, 0, 1, 1, atr14_values, "ATR14", reason))
      {
         policy_context = reason;
         return false;
      }
      if(!CopyIndicatorBufferWindow(g_handle_atr50, 0, 1, 1, atr50_values, "ATR50", reason))
      {
         policy_context = reason;
         return false;
      }

      const double atr14 = atr14_values[0];
      const double atr50 = atr50_values[0];
      if(!IsUsableValue(atr14) || !IsUsableValue(atr50) || atr14 <= 0.0 || atr50 <= 0.0)
      {
         policy_context = "STOP_REGIME_RATIO_INVALID";
         return false;
      }

      const double regime_ratio = atr14 / atr50;
      if(regime_ratio < g_effective_stop_low_vol_threshold)
      {
         atr_mult = g_effective_stop_low_atr_mult;
         policy_context = StringFormat("REGIME_LOW_%.4f", regime_ratio);
      }
      else if(regime_ratio > g_effective_stop_high_vol_threshold)
      {
         atr_mult = g_effective_stop_high_atr_mult;
         policy_context = StringFormat("REGIME_HIGH_%.4f", regime_ratio);
      }
      else
      {
         atr_mult = g_effective_stop_mid_atr_mult;
         policy_context = StringFormat("REGIME_MID_%.4f", regime_ratio);
      }
   }
   else
   {
      policy_context = "STOP_POLICY_UNSUPPORTED";
      return false;
   }

   if(!IsUsableValue(atr_mult) || atr_mult <= 0.0)
   {
      policy_context = "STOP_MULT_INVALID";
      return false;
   }
   return true;
}

datetime InferExitBarTimeServer(const datetime event_time_server)
{
   if(event_time_server <= 0)
      return 0;

   const int shift = iBarShift(_Symbol, PERIOD_M5, event_time_server, false);
   if(shift >= 0)
   {
      const datetime bar_open = iTime(_Symbol, PERIOD_M5, shift);
      if(bar_open > 0)
         return bar_open + PeriodSeconds(PERIOD_M5);
   }

   const datetime current_bar_open = iTime(_Symbol, PERIOD_M5, 0);
   if(current_bar_open > 0)
      return current_bar_open + PeriodSeconds(PERIOD_M5);
   return event_time_server;
}

string MapDealReasonToCloseReason(const long deal_reason)
{
   if(deal_reason == DEAL_REASON_SL)
      return "BROKER_SL";
   if(deal_reason == DEAL_REASON_TP)
      return "BROKER_TP";
   if(deal_reason == DEAL_REASON_SO)
      return "BROKER_STOP_OUT";
   if(deal_reason == DEAL_REASON_EXPERT)
      return "BROKER_EXPERT";
   if(deal_reason == DEAL_REASON_CLIENT)
      return "BROKER_CLIENT";
   if(deal_reason == DEAL_REASON_MOBILE)
      return "BROKER_MOBILE";
   if(deal_reason == DEAL_REASON_WEB)
      return "BROKER_WEB";
   return "BROKER_EXTERNAL_EXIT";
}

bool ResolveManagedCloseDealFromHistory(ulong &close_deal_ticket, string &close_reason, datetime &exit_bar_time_server)
{
   close_deal_ticket = 0;
   close_reason = "";
   exit_bar_time_server = 0;

   if(!g_managed_trade_active || g_managed_position_identifier <= 0)
      return false;

   if(!HistorySelect(g_managed_entry_time_server - 86400, TimeCurrent() + 60))
      return false;

   const int deal_count = HistoryDealsTotal();
   for(int i = deal_count - 1; i >= 0; i--)
   {
      const ulong deal_ticket = HistoryDealGetTicket(i);
      if(deal_ticket == 0 || deal_ticket == g_managed_entry_deal_ticket)
         continue;
      if((long)HistoryDealGetInteger(deal_ticket, DEAL_POSITION_ID) != g_managed_position_identifier)
         continue;

      const long deal_entry = HistoryDealGetInteger(deal_ticket, DEAL_ENTRY);
      if(deal_entry == DEAL_ENTRY_IN)
         continue;

      const datetime exit_time_server = (datetime)HistoryDealGetInteger(deal_ticket, DEAL_TIME);
      if(exit_time_server < g_managed_entry_time_server)
         continue;

      close_deal_ticket = deal_ticket;
      close_reason = MapDealReasonToCloseReason(HistoryDealGetInteger(deal_ticket, DEAL_REASON));
      exit_bar_time_server = InferExitBarTimeServer(exit_time_server);
      return true;
   }

   return false;
}

bool ComputeLossPerLotAtStop(
   const int decision,
   const double entry_price,
   const double stop_price,
   double &loss_per_lot,
   string &reason
)
{
   loss_per_lot = 0.0;
   const ENUM_ORDER_TYPE order_type = (decision > 0) ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;
   double pnl_per_lot = 0.0;
   ResetLastError();
   if(!OrderCalcProfit(order_type, _Symbol, 1.0, entry_price, stop_price, pnl_per_lot))
   {
      reason = StringFormat("ORDERCALC_STOP_FAIL_%d", GetLastError());
      return false;
   }

   loss_per_lot = MathAbs(pnl_per_lot);
   if(!IsUsableValue(loss_per_lot) || loss_per_lot <= 0.0)
   {
      reason = "LOSS_PER_LOT_INVALID";
      return false;
   }
   return true;
}

bool ComputeTradeExecutionPlan(
   const int decision,
   const datetime bar_time_server,
   double &planned_volume,
   double &planned_stop_price,
   double &planned_stop_distance_price,
   double &planned_stop_atr_mult,
   double &planned_risk_amount,
   double &planned_risk_pct_multiplier,
   string &planned_risk_context,
   string &reason
)
{
   planned_volume = 0.0;
   planned_stop_price = 0.0;
   planned_stop_distance_price = 0.0;
   planned_stop_atr_mult = 0.0;
   planned_risk_amount = 0.0;
   planned_risk_pct_multiplier = 1.0;
   planned_risk_context = "BASE";
   reason = "";

   if(g_effective_sizing_mode == "fixed_lot")
   {
      planned_volume = g_effective_fixed_lot;
      if(planned_volume <= 0.0)
         reason = "FIXED_LOT_INVALID";
      return (planned_volume > 0.0);
   }

   if(g_effective_sizing_mode != "risk_pct")
   {
      reason = "SIZING_MODE_UNSUPPORTED";
      return false;
   }

   if(g_effective_risk_pct <= 0.0)
   {
      reason = "RISK_PCT_INVALID";
      return false;
   }
   if(g_effective_stop_model != "atr")
   {
      reason = "STOP_MODEL_UNSUPPORTED";
      return false;
   }

   string stop_policy_context = "";
   if(!ResolveEffectiveStopAtrMult(decision, planned_stop_atr_mult, stop_policy_context))
   {
      reason = stop_policy_context;
      return false;
   }

   MqlTick tick;
   if(!SymbolInfoTick(_Symbol, tick))
   {
      reason = "SYMBOL_TICK_UNAVAILABLE";
      return false;
   }

   const double reference_entry_price = (decision > 0) ? tick.ask : tick.bid;
   if(!IsUsableValue(reference_entry_price) || reference_entry_price <= 0.0)
   {
      reason = "ENTRY_REFERENCE_PRICE_INVALID";
      return false;
   }

   if(!ComputeAtrStopDistancePrice(g_effective_stop_atr_period, planned_stop_atr_mult, planned_stop_distance_price, reason))
      return false;

   planned_stop_price = (decision > 0)
      ? (reference_entry_price - planned_stop_distance_price)
      : (reference_entry_price + planned_stop_distance_price);
   planned_stop_price = NormalizePriceForSymbol(planned_stop_price);
   planned_stop_distance_price = MathAbs(reference_entry_price - planned_stop_price);

   double loss_per_lot = 0.0;
   if(!ComputeLossPerLotAtStop(decision, reference_entry_price, planned_stop_price, loss_per_lot, reason))
      return false;

   const double capital_base = ResolveRiskCapitalBase();
   if(!IsUsableValue(capital_base) || capital_base <= 0.0)
   {
      reason = "RISK_CAPITAL_BASE_INVALID";
      return false;
   }

   planned_risk_amount = capital_base * (g_effective_risk_pct / 100.0);
   if(!IsUsableValue(planned_risk_amount) || planned_risk_amount <= 0.0)
   {
      reason = "RISK_AMOUNT_INVALID";
      return false;
   }

   planned_risk_pct_multiplier = ResolveDynamicRiskPctMultiplier(decision, bar_time_server, planned_risk_context);
   if(!IsUsableValue(planned_risk_pct_multiplier) || planned_risk_pct_multiplier <= 0.0)
   {
      reason = "RISK_MULTIPLIER_INVALID";
      return false;
   }

   planned_risk_amount *= planned_risk_pct_multiplier;
   if(!IsUsableValue(planned_risk_amount) || planned_risk_amount <= 0.0)
   {
      reason = "RISK_AMOUNT_ADJUSTED_INVALID";
      return false;
   }

   planned_volume = NormalizeVolumeForSymbol(planned_risk_amount / loss_per_lot);
   if(planned_volume <= 0.0)
      reason = "RISK_VOLUME_BELOW_MIN";
   return true;
}

bool EnsureExitRuleCapacity(const int rule_index)
{
   if(rule_index < 0)
      return false;

   const int current_size = ArraySize(g_effective_exit_rule_types);
   if(current_size > rule_index)
      return true;

   const int new_size = rule_index + 1;
   ArrayResize(g_effective_exit_rule_types, new_size);
   ArrayResize(g_effective_exit_rule_enabled, new_size);
   ArrayResize(g_effective_exit_rule_max_hold_bars, new_size);
   ArrayResize(g_effective_exit_rule_min_flat_probability, new_size);
   ArrayResize(g_effective_exit_rule_min_hold_bars, new_size);
   ArrayResize(g_effective_exit_rule_trigger_points, new_size);
   ArrayResize(g_effective_exit_rule_offset_points, new_size);
   ArrayResize(g_effective_exit_rule_distance_points, new_size);
   ArrayResize(g_effective_exit_rule_close_fraction, new_size);
   for(int i = current_size; i < new_size; i++)
   {
      g_effective_exit_rule_types[i] = "";
      g_effective_exit_rule_enabled[i] = true;
      g_effective_exit_rule_max_hold_bars[i] = 0;
      g_effective_exit_rule_min_flat_probability[i] = 0.0;
      g_effective_exit_rule_min_hold_bars[i] = 1;
      g_effective_exit_rule_trigger_points[i] = 0.0;
      g_effective_exit_rule_offset_points[i] = 0.0;
      g_effective_exit_rule_distance_points[i] = 0.0;
      g_effective_exit_rule_close_fraction[i] = 0.0;
   }
   return true;
}

void FinalizeExitRuleRuntimeConfig()
{
   g_effective_time_exit_enabled = false;
   g_effective_max_hold_bars = 3;
   g_effective_flat_exit_enabled = false;
   g_effective_flat_exit_min_probability = 0.0;
   g_effective_flat_exit_min_hold_bars = 1;

   const int exit_rule_count = ArraySize(g_effective_exit_rule_types);
   if(exit_rule_count <= 0)
   {
      g_effective_time_exit_enabled = true;
      return;
   }

   for(int i = 0; i < exit_rule_count; i++)
   {
      if(!g_effective_exit_rule_enabled[i])
         continue;

      const string rule_type = g_effective_exit_rule_types[i];
      if(rule_type == "time_exit")
      {
         g_effective_time_exit_enabled = true;
         if(g_effective_exit_rule_max_hold_bars[i] > 0)
            g_effective_max_hold_bars = g_effective_exit_rule_max_hold_bars[i];
      }
      else if(rule_type == "flat_exit_guard")
      {
         g_effective_flat_exit_enabled = true;
         g_effective_flat_exit_min_probability = g_effective_exit_rule_min_flat_probability[i];
         if(g_effective_exit_rule_min_hold_bars[i] > 0)
            g_effective_flat_exit_min_hold_bars = g_effective_exit_rule_min_hold_bars[i];
      }
   }
}

bool TryApplyExitRuleRuntimeKey(const string key, const string value)
{
   if(StringSubstr(key, 0, 5) != "exit_")
      return false;

   const int second_underscore = StringFind(key, "_", 5);
   if(second_underscore <= 5)
      return false;

   const string index_text = StringSubstr(key, 5, second_underscore - 5);
   const int rule_index = (int)StringToInteger(index_text);
   if(rule_index < 0 || !EnsureExitRuleCapacity(rule_index))
      return false;

   const string suffix = StringSubstr(key, second_underscore + 1);
   bool bool_value = false;
   if(suffix == "type")
   {
      g_effective_exit_rule_types[rule_index] = value;
      return true;
   }
   if(suffix == "enabled")
   {
      if(!ParseBoolText(value, bool_value))
         return false;
      g_effective_exit_rule_enabled[rule_index] = bool_value;
      return true;
   }
   if(suffix == "max_hold_bars")
   {
      g_effective_exit_rule_max_hold_bars[rule_index] = (int)StringToInteger(value);
      return true;
   }
   if(suffix == "min_flat_probability")
   {
      g_effective_exit_rule_min_flat_probability[rule_index] = StringToDouble(value);
      return true;
   }
   if(suffix == "min_hold_bars")
   {
      g_effective_exit_rule_min_hold_bars[rule_index] = (int)StringToInteger(value);
      return true;
   }
   if(suffix == "trigger_points")
   {
      g_effective_exit_rule_trigger_points[rule_index] = StringToDouble(value);
      return true;
   }
   if(suffix == "offset_points")
   {
      g_effective_exit_rule_offset_points[rule_index] = StringToDouble(value);
      return true;
   }
   if(suffix == "distance_points")
   {
      g_effective_exit_rule_distance_points[rule_index] = StringToDouble(value);
      return true;
   }
   if(suffix == "close_fraction")
   {
      g_effective_exit_rule_close_fraction[rule_index] = StringToDouble(value);
      return true;
   }
   return false;
}

void ResetEffectiveRuntimeConfig()
{
   g_effective_feature_count = OP_FEATURE_COUNT;
   ArrayResize(g_effective_feature_names, 0);
   g_effective_onnx_model_path = InpOnnxModelPath;
   g_effective_onnx_use_common_files = InpOnnxUseCommonFiles;
   g_effective_short_threshold = InpShortThreshold;
   g_effective_long_threshold = InpLongThreshold;
   g_effective_min_margin = InpMinMargin;
   g_effective_min_probability_diff = 0.0;
   g_effective_sizing_mode = "fixed_lot";
   g_effective_fixed_lot = InpFixedLot;
   g_effective_risk_pct = 0.0;
   g_effective_capital_base = "balance";
   g_effective_monday_risk_pct_mult = 1.0;
   g_effective_ny_postcash_risk_pct_mult = 1.0;
   g_effective_monday_long_risk_pct_mult = 1.0;
   g_effective_monday_short_risk_pct_mult = 1.0;
   g_effective_ny_postcash_hold_cap_bars = 0;
   g_effective_ny_clock_taper_start_minute = -1;
   g_effective_ny_clock_taper_mid_minute = -1;
   g_effective_ny_clock_taper_late_minute = -1;
   g_effective_ny_clock_taper_start_mult = 1.0;
   g_effective_ny_clock_taper_mid_mult = 1.0;
   g_effective_ny_clock_taper_late_mult = 1.0;
   g_effective_stop_model = "";
   g_effective_stop_execution_mode = "ea_managed";
   g_effective_stop_policy = "fixed";
   g_effective_stop_atr_period = 14;
   g_effective_stop_atr_mult = 0.0;
   g_effective_stop_long_atr_mult = 0.0;
   g_effective_stop_short_atr_mult = 0.0;
   g_effective_stop_low_vol_threshold = 0.0;
   g_effective_stop_high_vol_threshold = 0.0;
   g_effective_stop_low_atr_mult = 0.0;
   g_effective_stop_mid_atr_mult = 0.0;
   g_effective_stop_high_atr_mult = 0.0;
   g_effective_external_alignment_mode = "exact";
   g_effective_external_relaxed_scope = "none";
   g_effective_external_max_stale_bars = 0;
   g_effective_max_hold_bars = 3;
   g_effective_max_concurrent_positions = 1;
   g_effective_time_exit_enabled = true;
   g_effective_flat_exit_enabled = false;
   g_effective_flat_exit_min_probability = 0.0;
   g_effective_flat_exit_min_hold_bars = 1;
   g_effective_threshold_rule_enabled = true;
   g_effective_margin_rule_enabled = (InpMinMargin > 0.0);
   g_effective_prob_diff_rule_enabled = false;
   g_effective_experiment_id = "";
   g_effective_bundle_version = "";
   g_effective_logic_family = "";
   g_effective_feature_fingerprint = "";
   ArrayResize(g_effective_exit_rule_types, 0);
   ArrayResize(g_effective_exit_rule_enabled, 0);
   ArrayResize(g_effective_exit_rule_max_hold_bars, 0);
   ArrayResize(g_effective_exit_rule_min_flat_probability, 0);
   ArrayResize(g_effective_exit_rule_min_hold_bars, 0);
   ArrayResize(g_effective_exit_rule_trigger_points, 0);
   ArrayResize(g_effective_exit_rule_offset_points, 0);
   ArrayResize(g_effective_exit_rule_distance_points, 0);
   ArrayResize(g_effective_exit_rule_close_fraction, 0);
   g_runtime_config_loaded = false;
}

int FindActiveFeatureIndex(const string feature_name)
{
   const int feature_name_count = ArraySize(g_effective_feature_names);
   for(int i = 0; i < feature_name_count; i++)
   {
      if(g_effective_feature_names[i] == feature_name)
         return i;
   }
   return -1;
}

bool TryAssignActiveFeatureValue(
   double &features[],
   int &feature_ready_count,
   const string feature_name,
   const double value,
   string &skip_reason
)
{
   const int feature_index = FindActiveFeatureIndex(feature_name);
   if(feature_index < 0)
      return true;

   if(!IsUsableValue(value))
   {
      skip_reason = "FEATURE_VALUE_INVALID_" + feature_name;
      return false;
   }

   features[feature_index] = value;
   feature_ready_count++;
   return true;
}

bool IsFeatureRequested(const string feature_name)
{
   const int feature_name_count = ArraySize(g_effective_feature_names);
   if(feature_name_count <= 0)
      return true;
   return (FindActiveFeatureIndex(feature_name) >= 0);
}

bool ApplyRuntimeConfigKeyValue(const string key, const string value)
{
   bool bool_value = false;
   if(key == "experiment_id")
   {
      g_effective_experiment_id = value;
      return true;
   }
   if(key == "bundle_version")
   {
      g_effective_bundle_version = value;
      return true;
   }
   if(key == "logic_family")
   {
      g_effective_logic_family = value;
      return true;
   }
   if(key == "feature_fingerprint")
   {
      g_effective_feature_fingerprint = value;
      return true;
   }
   if(key == "feature_count")
   {
      g_effective_feature_count = (int)StringToInteger(value);
      return (g_effective_feature_count > 0);
   }
   if(key == "onnx_model_path")
   {
      g_effective_onnx_model_path = value;
      return true;
   }
   if(StringFind(key, "feature_") == 0)
   {
      const int suffix_index = StringFind(key, "_name", 8);
      if(suffix_index > 8 && suffix_index == (StringLen(key) - 5))
      {
         const string index_text = StringSubstr(key, 8, suffix_index - 8);
         const int feature_index = (int)StringToInteger(index_text);
         if(feature_index < 0)
            return false;
         if(ArraySize(g_effective_feature_names) <= feature_index)
            ArrayResize(g_effective_feature_names, feature_index + 1);
         g_effective_feature_names[feature_index] = value;
         return true;
      }
   }
   if(key == "onnx_use_common_files")
   {
      return ParseBoolText(value, g_effective_onnx_use_common_files);
   }
   if(key == "entry_0_enabled")
   {
      return ParseBoolText(value, g_effective_threshold_rule_enabled);
   }
   if(key == "entry_0_short_threshold")
   {
      g_effective_short_threshold = StringToDouble(value);
      return true;
   }
   if(key == "entry_0_long_threshold")
   {
      g_effective_long_threshold = StringToDouble(value);
      return true;
   }
   if(key == "filters_0_type")
   {
      if(value == "max_probability_margin")
         g_effective_margin_rule_enabled = true;
      if(value == "probability_difference")
         g_effective_prob_diff_rule_enabled = true;
      return true;
   }
   if(key == "filters_0_enabled")
   {
      if(!ParseBoolText(value, bool_value))
         return false;
      if(!bool_value)
      {
         g_effective_margin_rule_enabled = false;
         g_effective_prob_diff_rule_enabled = false;
      }
      return true;
   }
   if(key == "filters_0_min_margin")
   {
      g_effective_margin_rule_enabled = true;
      g_effective_min_margin = StringToDouble(value);
      return true;
   }
   if(key == "filters_0_min_probability_diff")
   {
      g_effective_prob_diff_rule_enabled = true;
      g_effective_min_probability_diff = StringToDouble(value);
      return true;
   }
   if(key == "fixed_lot")
   {
      g_effective_fixed_lot = StringToDouble(value);
      return (g_effective_fixed_lot > 0.0);
   }
   if(key == "sizing_mode")
   {
      g_effective_sizing_mode = value;
      StringToLower(g_effective_sizing_mode);
      return true;
   }
   if(key == "risk_pct")
   {
      g_effective_risk_pct = StringToDouble(value);
      return true;
   }
   if(key == "capital_base")
   {
      g_effective_capital_base = value;
      StringToLower(g_effective_capital_base);
      return true;
   }
   if(key == "monday_risk_pct_mult")
   {
      g_effective_monday_risk_pct_mult = StringToDouble(value);
      return true;
   }
   if(key == "monday_long_risk_pct_mult")
   {
      g_effective_monday_long_risk_pct_mult = StringToDouble(value);
      return true;
   }
   if(key == "monday_short_risk_pct_mult")
   {
      g_effective_monday_short_risk_pct_mult = StringToDouble(value);
      return true;
   }
   if(key == "ny_postcash_risk_pct_mult")
   {
      g_effective_ny_postcash_risk_pct_mult = StringToDouble(value);
      return true;
   }
   if(key == "ny_postcash_hold_cap_bars")
   {
      g_effective_ny_postcash_hold_cap_bars = (int)StringToInteger(value);
      return true;
   }
   if(key == "ny_clock_taper_start_minute")
   {
      g_effective_ny_clock_taper_start_minute = (int)StringToInteger(value);
      return true;
   }
   if(key == "ny_clock_taper_mid_minute")
   {
      g_effective_ny_clock_taper_mid_minute = (int)StringToInteger(value);
      return true;
   }
   if(key == "ny_clock_taper_late_minute")
   {
      g_effective_ny_clock_taper_late_minute = (int)StringToInteger(value);
      return true;
   }
   if(key == "ny_clock_taper_start_mult")
   {
      g_effective_ny_clock_taper_start_mult = StringToDouble(value);
      return true;
   }
   if(key == "ny_clock_taper_mid_mult")
   {
      g_effective_ny_clock_taper_mid_mult = StringToDouble(value);
      return true;
   }
   if(key == "ny_clock_taper_late_mult")
   {
      g_effective_ny_clock_taper_late_mult = StringToDouble(value);
      return true;
   }
   if(key == "stop_model")
   {
      g_effective_stop_model = value;
      StringToLower(g_effective_stop_model);
      return true;
   }
   if(key == "stop_execution_mode")
   {
      g_effective_stop_execution_mode = value;
      StringToLower(g_effective_stop_execution_mode);
      return true;
   }
   if(key == "stop_policy")
   {
      g_effective_stop_policy = value;
      StringToLower(g_effective_stop_policy);
      return true;
   }
   if(key == "stop_atr_period")
   {
      g_effective_stop_atr_period = (int)StringToInteger(value);
      return true;
   }
   if(key == "stop_atr_mult")
   {
      g_effective_stop_atr_mult = StringToDouble(value);
      return true;
   }
   if(key == "stop_long_atr_mult")
   {
      g_effective_stop_long_atr_mult = StringToDouble(value);
      return true;
   }
   if(key == "stop_short_atr_mult")
   {
      g_effective_stop_short_atr_mult = StringToDouble(value);
      return true;
   }
   if(key == "stop_low_vol_threshold")
   {
      g_effective_stop_low_vol_threshold = StringToDouble(value);
      return true;
   }
   if(key == "stop_high_vol_threshold")
   {
      g_effective_stop_high_vol_threshold = StringToDouble(value);
      return true;
   }
   if(key == "stop_low_atr_mult")
   {
      g_effective_stop_low_atr_mult = StringToDouble(value);
      return true;
   }
   if(key == "stop_mid_atr_mult")
   {
      g_effective_stop_mid_atr_mult = StringToDouble(value);
      return true;
   }
   if(key == "stop_high_atr_mult")
   {
      g_effective_stop_high_atr_mult = StringToDouble(value);
      return true;
   }
   if(key == "external_alignment_mode")
   {
      g_effective_external_alignment_mode = value;
      StringToLower(g_effective_external_alignment_mode);
      return true;
   }
   if(key == "external_relaxed_scope")
   {
      g_effective_external_relaxed_scope = value;
      StringToLower(g_effective_external_relaxed_scope);
      return true;
   }
   if(key == "external_max_stale_bars")
   {
      g_effective_external_max_stale_bars = (int)StringToInteger(value);
      return true;
   }
   if(key == "position_0_enabled")
   {
      return ParseBoolText(value, bool_value);
   }
   if(key == "position_0_max_concurrent_positions")
   {
      g_effective_max_concurrent_positions = (int)StringToInteger(value);
      return true;
   }
   if(TryApplyExitRuleRuntimeKey(key, value))
      return true;
   return true;
}

bool LoadRuntimeConfig()
{
   ResetEffectiveRuntimeConfig();
   if(!InpUseRuntimeConfig)
      return true;

   int flags = FILE_READ | FILE_TXT | FILE_ANSI;
   if(InpRuntimeConfigUseCommonFiles)
      flags |= FILE_COMMON;

   ResetLastError();
   int handle = FileOpen(InpRuntimeConfigPath, flags);
   if(handle == INVALID_HANDLE)
   {
      Log(StringFormat("failed to open runtime config err=%d path=%s", GetLastError(), InpRuntimeConfigPath));
      return false;
   }

   while(!FileIsEnding(handle))
   {
      string line = TrimText(FileReadString(handle));
      if(line == "" || StringSubstr(line, 0, 1) == "#")
         continue;

      int eq_index = StringFind(line, "=");
      if(eq_index <= 0)
         continue;

      string key = TrimText(StringSubstr(line, 0, eq_index));
      string value = TrimText(StringSubstr(line, eq_index + 1));
      if(!ApplyRuntimeConfigKeyValue(key, value))
      {
         FileClose(handle);
         Log(StringFormat("failed to parse runtime config key=%s value=%s", key, value));
         return false;
      }
   }

   FileClose(handle);
   if(g_effective_feature_count <= 0)
   {
      Log("runtime config has invalid feature_count");
      return false;
   }
   const int runtime_feature_name_count = ArraySize(g_effective_feature_names);
   if(runtime_feature_name_count > 0 && runtime_feature_name_count != g_effective_feature_count)
   {
      Log(StringFormat(
         "runtime config feature_name count mismatch expected=%d actual=%d",
         g_effective_feature_count,
         runtime_feature_name_count
      ));
      return false;
   }
   FinalizeExitRuleRuntimeConfig();
   if(g_effective_sizing_mode == "fixed_lot" && g_effective_fixed_lot <= 0.0)
   {
      Log("runtime config has invalid fixed_lot for fixed_lot sizing");
      return false;
   }
   if(g_effective_sizing_mode == "risk_pct")
   {
      if(g_effective_risk_pct <= 0.0)
      {
         Log("runtime config has invalid risk_pct for risk_pct sizing");
         return false;
      }
      if(g_effective_stop_model != "atr")
      {
         Log("runtime config has unsupported stop_model for risk_pct sizing");
         return false;
      }
      if(g_effective_stop_execution_mode != "ea_managed" && g_effective_stop_execution_mode != "broker_native")
      {
         Log("runtime config has unsupported stop_execution_mode for risk_pct sizing");
         return false;
      }
      if(g_effective_stop_policy != "fixed" &&
         g_effective_stop_policy != "regime_bucket" &&
         g_effective_stop_policy != "direction_split")
      {
         Log("runtime config has unsupported stop_policy for risk_pct sizing");
         return false;
      }
      if(g_effective_stop_atr_period <= 0 || !IsSupportedAtrPeriod(g_effective_stop_atr_period))
      {
         Log("runtime config has unsupported stop_atr_period for risk_pct sizing");
         return false;
      }
      if(g_effective_stop_policy == "fixed" && g_effective_stop_atr_mult <= 0.0)
      {
         Log("runtime config has invalid stop_atr_mult for fixed risk_pct sizing");
         return false;
      }
      if(g_effective_stop_policy == "direction_split" &&
         (g_effective_stop_long_atr_mult <= 0.0 || g_effective_stop_short_atr_mult <= 0.0))
      {
         Log("runtime config has invalid long/short ATR multipliers for direction_split sizing");
         return false;
      }
      if(g_effective_stop_policy == "regime_bucket")
      {
         if(g_effective_stop_low_vol_threshold >= g_effective_stop_high_vol_threshold)
         {
            Log("runtime config has invalid volatility thresholds for regime_bucket sizing");
            return false;
         }
         if(g_effective_stop_low_atr_mult <= 0.0 ||
            g_effective_stop_mid_atr_mult <= 0.0 ||
            g_effective_stop_high_atr_mult <= 0.0)
         {
            Log("runtime config has invalid ATR multipliers for regime_bucket sizing");
            return false;
         }
      }
      if(g_effective_stop_policy != "fixed" && g_effective_stop_atr_mult <= 0.0)
         g_effective_stop_atr_mult = 1.0;
      if(g_effective_monday_risk_pct_mult <= 0.0)
      {
         Log("runtime config has invalid monday_risk_pct_mult for risk_pct sizing");
         return false;
      }
      if(g_effective_monday_long_risk_pct_mult <= 0.0)
      {
         Log("runtime config has invalid monday_long_risk_pct_mult for risk_pct sizing");
         return false;
      }
      if(g_effective_monday_short_risk_pct_mult <= 0.0)
      {
         Log("runtime config has invalid monday_short_risk_pct_mult for risk_pct sizing");
         return false;
      }
      if(g_effective_ny_postcash_risk_pct_mult <= 0.0)
      {
         Log("runtime config has invalid ny_postcash_risk_pct_mult for risk_pct sizing");
         return false;
      }
      if(g_effective_ny_postcash_hold_cap_bars < 0)
      {
         Log("runtime config has invalid ny_postcash_hold_cap_bars for risk_pct sizing");
         return false;
      }
      if(g_effective_ny_clock_taper_start_minute >= 0 ||
         g_effective_ny_clock_taper_mid_minute >= 0 ||
         g_effective_ny_clock_taper_late_minute >= 0)
      {
         if(g_effective_ny_clock_taper_start_minute < 0 ||
            g_effective_ny_clock_taper_mid_minute < 0 ||
            g_effective_ny_clock_taper_late_minute < 0 ||
            g_effective_ny_clock_taper_start_minute >= g_effective_ny_clock_taper_mid_minute ||
            g_effective_ny_clock_taper_mid_minute >= g_effective_ny_clock_taper_late_minute)
         {
            Log("runtime config has invalid ny_clock_taper minute thresholds");
            return false;
         }
         if(g_effective_ny_clock_taper_start_mult <= 0.0 ||
            g_effective_ny_clock_taper_mid_mult <= 0.0 ||
            g_effective_ny_clock_taper_late_mult <= 0.0)
         {
            Log("runtime config has invalid ny_clock_taper multipliers");
            return false;
         }
      }
   }
   g_runtime_config_loaded = true;
   Log(StringFormat(
      "runtime config loaded experiment=%s logic=%s onnx=%s feature_count=%d sizing_mode=%s fixed_lot=%.4f risk_pct=%.4f capital_base=%s monday_risk_mult=%.4f monday_long_mult=%.4f monday_short_mult=%.4f ny_postcash_risk_mult=%.4f ny_postcash_hold_cap=%d taper_start=%d taper_mid=%d taper_late=%d taper_mults=%.4f/%.4f/%.4f stop_model=%s stop_execution_mode=%s stop_policy=%s stop_atr_period=%d stop_atr_mult=%.4f long_mult=%.4f short_mult=%.4f low_thr=%.4f high_thr=%.4f low_mult=%.4f mid_mult=%.4f high_mult=%.4f threshold_enabled=%s short=%.6f long=%.6f margin_enabled=%s margin=%.6f diff_enabled=%s diff=%.6f time_exit=%s hold=%d flat_exit=%s flat_min=%.6f flat_min_hold=%d",
      g_effective_experiment_id,
      g_effective_logic_family,
      g_effective_onnx_model_path,
      g_effective_feature_count,
      g_effective_sizing_mode,
      g_effective_fixed_lot,
      g_effective_risk_pct,
      g_effective_capital_base,
      g_effective_monday_risk_pct_mult,
      g_effective_monday_long_risk_pct_mult,
      g_effective_monday_short_risk_pct_mult,
      g_effective_ny_postcash_risk_pct_mult,
      g_effective_ny_postcash_hold_cap_bars,
      g_effective_ny_clock_taper_start_minute,
      g_effective_ny_clock_taper_mid_minute,
      g_effective_ny_clock_taper_late_minute,
      g_effective_ny_clock_taper_start_mult,
      g_effective_ny_clock_taper_mid_mult,
      g_effective_ny_clock_taper_late_mult,
      g_effective_stop_model,
      g_effective_stop_execution_mode,
      g_effective_stop_policy,
      g_effective_stop_atr_period,
      g_effective_stop_atr_mult,
      g_effective_stop_long_atr_mult,
      g_effective_stop_short_atr_mult,
      g_effective_stop_low_vol_threshold,
      g_effective_stop_high_vol_threshold,
      g_effective_stop_low_atr_mult,
      g_effective_stop_mid_atr_mult,
      g_effective_stop_high_atr_mult,
      g_effective_threshold_rule_enabled ? "true" : "false",
      g_effective_short_threshold,
      g_effective_long_threshold,
      g_effective_margin_rule_enabled ? "true" : "false",
      g_effective_min_margin,
      g_effective_prob_diff_rule_enabled ? "true" : "false",
      g_effective_min_probability_diff,
      g_effective_time_exit_enabled ? "true" : "false",
      g_effective_max_hold_bars
      ,
      g_effective_flat_exit_enabled ? "true" : "false",
      g_effective_flat_exit_min_probability,
      g_effective_flat_exit_min_hold_bars
   ));
   return true;
}

void ReleaseIndicatorHandles()
{
   if(g_handle_ema9 != INVALID_HANDLE)
      IndicatorRelease(g_handle_ema9);
   if(g_handle_ema20 != INVALID_HANDLE)
      IndicatorRelease(g_handle_ema20);
   if(g_handle_ema50 != INVALID_HANDLE)
      IndicatorRelease(g_handle_ema50);
   if(g_handle_ema200 != INVALID_HANDLE)
      IndicatorRelease(g_handle_ema200);
   if(g_handle_sma50 != INVALID_HANDLE)
      IndicatorRelease(g_handle_sma50);
   if(g_handle_sma200 != INVALID_HANDLE)
      IndicatorRelease(g_handle_sma200);
   if(g_handle_rsi14 != INVALID_HANDLE)
      IndicatorRelease(g_handle_rsi14);
   if(g_handle_rsi50 != INVALID_HANDLE)
      IndicatorRelease(g_handle_rsi50);
   if(g_handle_atr14 != INVALID_HANDLE)
      IndicatorRelease(g_handle_atr14);
   if(g_handle_atr20 != INVALID_HANDLE)
      IndicatorRelease(g_handle_atr20);
   if(g_handle_atr50 != INVALID_HANDLE)
      IndicatorRelease(g_handle_atr50);
   if(g_handle_bands20 != INVALID_HANDLE)
      IndicatorRelease(g_handle_bands20);
   if(g_handle_adx14 != INVALID_HANDLE)
      IndicatorRelease(g_handle_adx14);
   if(g_handle_stoch14 != INVALID_HANDLE)
      IndicatorRelease(g_handle_stoch14);

   g_handle_ema9 = INVALID_HANDLE;
   g_handle_ema20 = INVALID_HANDLE;
   g_handle_ema50 = INVALID_HANDLE;
   g_handle_ema200 = INVALID_HANDLE;
   g_handle_sma50 = INVALID_HANDLE;
   g_handle_sma200 = INVALID_HANDLE;
   g_handle_rsi14 = INVALID_HANDLE;
   g_handle_rsi50 = INVALID_HANDLE;
   g_handle_atr14 = INVALID_HANDLE;
   g_handle_atr20 = INVALID_HANDLE;
   g_handle_atr50 = INVALID_HANDLE;
   g_handle_bands20 = INVALID_HANDLE;
   g_handle_adx14 = INVALID_HANDLE;
   g_handle_stoch14 = INVALID_HANDLE;
}

bool CreateIndicatorHandles()
{
   ReleaseIndicatorHandles();

   g_handle_ema9 = iMA(_Symbol, PERIOD_M5, 9, 0, MODE_EMA, PRICE_CLOSE);
   g_handle_ema20 = iMA(_Symbol, PERIOD_M5, 20, 0, MODE_EMA, PRICE_CLOSE);
   g_handle_ema50 = iMA(_Symbol, PERIOD_M5, 50, 0, MODE_EMA, PRICE_CLOSE);
   g_handle_ema200 = iMA(_Symbol, PERIOD_M5, 200, 0, MODE_EMA, PRICE_CLOSE);
   g_handle_sma50 = iMA(_Symbol, PERIOD_M5, 50, 0, MODE_SMA, PRICE_CLOSE);
   g_handle_sma200 = iMA(_Symbol, PERIOD_M5, 200, 0, MODE_SMA, PRICE_CLOSE);
   g_handle_rsi14 = iRSI(_Symbol, PERIOD_M5, 14, PRICE_CLOSE);
   g_handle_rsi50 = iRSI(_Symbol, PERIOD_M5, 50, PRICE_CLOSE);
   g_handle_atr14 = iATR(_Symbol, PERIOD_M5, 14);
   g_handle_atr20 = iATR(_Symbol, PERIOD_M5, 20);
   g_handle_atr50 = iATR(_Symbol, PERIOD_M5, 50);
   g_handle_bands20 = iBands(_Symbol, PERIOD_M5, 20, 0, 2.0, PRICE_CLOSE);
   g_handle_adx14 = iADX(_Symbol, PERIOD_M5, 14);
   g_handle_stoch14 = iStochastic(_Symbol, PERIOD_M5, 14, 3, 3, MODE_SMA, STO_LOWHIGH);

   if(g_handle_ema9 == INVALID_HANDLE ||
      g_handle_ema20 == INVALID_HANDLE ||
      g_handle_ema50 == INVALID_HANDLE ||
      g_handle_ema200 == INVALID_HANDLE ||
      g_handle_sma50 == INVALID_HANDLE ||
      g_handle_sma200 == INVALID_HANDLE ||
      g_handle_rsi14 == INVALID_HANDLE ||
      g_handle_rsi50 == INVALID_HANDLE ||
      g_handle_atr14 == INVALID_HANDLE ||
      g_handle_atr20 == INVALID_HANDLE ||
      g_handle_atr50 == INVALID_HANDLE ||
      g_handle_bands20 == INVALID_HANDLE ||
      g_handle_adx14 == INVALID_HANDLE ||
      g_handle_stoch14 == INVALID_HANDLE)
   {
      Log(StringFormat("indicator handle creation failed err=%d", GetLastError()));
      ReleaseIndicatorHandles();
      return false;
   }

   return true;
}

void Log(const string message)
{
   if(InpVerboseLog)
      Print("[ObsidianPrime][Stage1] ", message);
}

string FeatureModeToString(const ENUM_OP_FEATURE_MODE mode)
{
   switch(mode)
   {
      case OP_FEATURE_MODE_ZERO_SMOKE:
         return "ZERO_SMOKE";
      case OP_FEATURE_MODE_PRICE_CORE_PARTIAL:
         return "PRICE_CORE_PARTIAL";
      case OP_FEATURE_MODE_SKIP_UNIMPLEMENTED:
         return "SKIP_UNIMPLEMENTED";
   }
   return "UNKNOWN";
}

string DecisionToString(const int decision)
{
   if(decision > 0)
      return "LONG";
   if(decision < 0)
      return "SHORT";
   return "NO_TRADE";
}

string EscapeCsv(const string value)
{
   string escaped = value;
   StringReplace(escaped, "\"", "\"\"");
   return "\"" + escaped + "\"";
}

string CsvDouble(const double value, const int digits = 6)
{
   if(!IsUsableValue(value))
      return "";
   return DoubleToString(value, digits);
}

string CsvInteger(const long value)
{
   return (string)value;
}

bool TextStartsWith(const string value, const string prefix)
{
   if(StringLen(prefix) <= 0)
      return true;
   if(StringLen(value) < StringLen(prefix))
      return false;
   return (StringFind(value, prefix) == 0);
}

void AppendGovernanceReasonTag(string &tags, const string tag)
{
   if(StringLen(tag) <= 0)
      return;
   if(StringLen(tags) > 0)
      tags += "|";
   tags += tag;
}

string GovernanceSkipCategoryToString(const int category)
{
   switch(category)
   {
      case OP_GOV_SKIP_NONE:
         return "NONE";
      case OP_GOV_SKIP_WARMUP:
         return "WARMUP";
      case OP_GOV_SKIP_EXTERNAL:
         return "EXTERNAL";
      case OP_GOV_SKIP_FEATURE:
         return "FEATURE";
      case OP_GOV_SKIP_RUNTIME:
         return "RUNTIME";
      case OP_GOV_SKIP_OTHER:
         return "OTHER";
   }
   return "UNKNOWN";
}

bool IsOperationalGovernanceSkipCategory(const int category)
{
   return (category == OP_GOV_SKIP_EXTERNAL ||
      category == OP_GOV_SKIP_FEATURE ||
      category == OP_GOV_SKIP_RUNTIME ||
      category == OP_GOV_SKIP_OTHER);
}

int ClassifyGovernanceSkipCategory(const string skip_reason)
{
   if(StringLen(skip_reason) <= 0)
      return OP_GOV_SKIP_NONE;

   if(TextStartsWith(skip_reason, "EXTERNAL_"))
      return OP_GOV_SKIP_EXTERNAL;

   if(skip_reason == "WARMUP_NOT_READY" ||
      TextStartsWith(skip_reason, "PRICE_CORE_WARMUP_") ||
      TextStartsWith(skip_reason, "RATES_NOT_READY_") ||
      TextStartsWith(skip_reason, "HANDLE_NOT_READY_") ||
      TextStartsWith(skip_reason, "HANDLE_INVALID_") ||
      TextStartsWith(skip_reason, "SESSION_"))
   {
      return OP_GOV_SKIP_WARMUP;
   }

   if(skip_reason == "PARTIAL_FEATURE_VECTOR" ||
      skip_reason == "FEATURE_SCHEMA_NAMES_NOT_READY" ||
      skip_reason == "PRICE_CORE_BAR_MISMATCH" ||
      TextStartsWith(skip_reason, "FEATURE_") ||
      TextStartsWith(skip_reason, "PRICE_CORE_INVALID_") ||
      TextStartsWith(skip_reason, "COPYBUFFER_FAIL_") ||
      TextStartsWith(skip_reason, "INDICATOR_INVALID_") ||
      TextStartsWith(skip_reason, "CUSTOM_"))
   {
      return OP_GOV_SKIP_FEATURE;
   }

   if(skip_reason == "SYMBOL_NOT_US100" ||
      skip_reason == "TIMEFRAME_NOT_M5" ||
      skip_reason == "MODEL_NOT_READY" ||
      skip_reason == "MODEL_HANDLE_INVALID" ||
      skip_reason == "FEATURE_BUILDER_NOT_IMPLEMENTED" ||
      TextStartsWith(skip_reason, "ONNX_") ||
      TextStartsWith(skip_reason, "OUTPUT_INVALID_"))
   {
      return OP_GOV_SKIP_RUNTIME;
   }

   return OP_GOV_SKIP_OTHER;
}

int ResolveArgmaxClass(const double p_short, const double p_flat, const double p_long)
{
   if(!IsUsableValue(p_short) || !IsUsableValue(p_flat) || !IsUsableValue(p_long))
      return -1;

   if(p_short >= p_flat && p_short >= p_long)
      return 0;
   if(p_flat >= p_short && p_flat >= p_long)
      return 1;
   return 2;
}

string ArgmaxClassToString(const int argmax_class)
{
   switch(argmax_class)
   {
      case 0:
         return "SHORT";
      case 1:
         return "FLAT";
      case 2:
         return "LONG";
   }
   return "";
}

double ComputeNormalizedSignalEntropy(const double p_short, const double p_flat, const double p_long)
{
   if(!IsUsableValue(p_short) || !IsUsableValue(p_flat) || !IsUsableValue(p_long))
      return EMPTY_VALUE;

   double total = p_short + p_flat + p_long;
   if(total <= 0.0)
      return EMPTY_VALUE;

   double entropy = 0.0;
   double probabilities[3];
   probabilities[0] = p_short / total;
   probabilities[1] = p_flat / total;
   probabilities[2] = p_long / total;
   for(int i = 0; i < 3; i++)
   {
      if(probabilities[i] > 0.0)
         entropy -= probabilities[i] * MathLog(probabilities[i]);
   }

   const double max_entropy = MathLog(3.0);
   if(max_entropy <= 0.0)
      return EMPTY_VALUE;
   return entropy / max_entropy;
}

double ComputeNormalizedMaxProbability(const double p_short, const double p_flat, const double p_long)
{
   if(!IsUsableValue(p_short) || !IsUsableValue(p_flat) || !IsUsableValue(p_long))
      return EMPTY_VALUE;

   double total = p_short + p_flat + p_long;
   if(total <= 0.0)
      return EMPTY_VALUE;
   return MathMax(p_short, MathMax(p_flat, p_long)) / total;
}

void ResetGovernanceState()
{
   ArrayResize(g_governance_skip_category_window, 0);
   ArrayResize(g_governance_inference_ready_window, 0);
   ArrayResize(g_governance_argmax_window, 0);
   ArrayResize(g_governance_extreme_confidence_window, 0);
   ArrayResize(g_governance_entropy_window, 0);
   ArrayResize(g_governance_signal_window, 0);
   ArrayResize(g_governance_overlay_window, 0);

   if(InpEnableGovernance && InpGovernanceWindowBars > 0)
   {
      ArrayResize(g_governance_skip_category_window, InpGovernanceWindowBars);
      ArrayResize(g_governance_inference_ready_window, InpGovernanceWindowBars);
      ArrayResize(g_governance_argmax_window, InpGovernanceWindowBars);
      ArrayResize(g_governance_extreme_confidence_window, InpGovernanceWindowBars);
      ArrayResize(g_governance_entropy_window, InpGovernanceWindowBars);
      ArrayResize(g_governance_signal_window, InpGovernanceWindowBars);
      ArrayResize(g_governance_overlay_window, InpGovernanceWindowBars);
      ArrayInitialize(g_governance_skip_category_window, OP_GOV_SKIP_NONE);
      ArrayInitialize(g_governance_inference_ready_window, 0);
      ArrayInitialize(g_governance_argmax_window, -1);
      ArrayInitialize(g_governance_extreme_confidence_window, 0);
      ArrayInitialize(g_governance_entropy_window, EMPTY_VALUE);
      ArrayInitialize(g_governance_signal_window, 0);
      ArrayInitialize(g_governance_overlay_window, 0);
   }

   g_governance_window_slot = 0;
   g_governance_window_count = 0;
   g_governance_state = InpEnableGovernance ? "WARMING_UP" : "DISABLED";
   g_governance_reason = InpEnableGovernance ? "INSUFFICIENT_SAMPLES" : "GOVERNANCE_DISABLED";
   g_governance_entry_blocked = false;
   g_governance_window_samples = 0;
   g_governance_inference_samples = 0;
   g_governance_signal_samples = 0;
   g_governance_consecutive_operational_skips = 0;
   g_governance_operational_skip_rate = 0.0;
   g_governance_external_skip_rate = 0.0;
   g_governance_feature_skip_rate = 0.0;
   g_governance_warmup_skip_rate = 0.0;
   g_governance_max_argmax_class_share = 0.0;
   g_governance_extreme_confidence_rate = 0.0;
   g_governance_avg_signal_entropy = EMPTY_VALUE;
   g_governance_risk_overlay_rate = EMPTY_VALUE;
   g_governance_current_skip_category = "NONE";
   g_governance_current_argmax_class = "";
   g_governance_current_signal_entropy = EMPTY_VALUE;
   g_governance_current_max_probability = EMPTY_VALUE;
   g_governance_current_extreme_confidence = false;
   g_governance_current_risk_context = "BASE";
   g_governance_current_risk_pct_multiplier = 1.0;
}

void RecordGovernanceObservation(
   const string skip_reason,
   const bool row_ready,
   const double p_short,
   const double p_flat,
   const double p_long,
   const int decision,
   const string planned_risk_context,
   const double planned_risk_pct_multiplier
)
{
   g_governance_current_skip_category = GovernanceSkipCategoryToString(ClassifyGovernanceSkipCategory(skip_reason));
   g_governance_current_argmax_class = "";
   g_governance_current_signal_entropy = EMPTY_VALUE;
   g_governance_current_max_probability = EMPTY_VALUE;
   g_governance_current_extreme_confidence = false;
   g_governance_current_risk_context = planned_risk_context;
   g_governance_current_risk_pct_multiplier = planned_risk_pct_multiplier;

   if(!InpEnableGovernance || InpGovernanceWindowBars <= 0)
   {
      g_governance_state = "DISABLED";
      g_governance_reason = "GOVERNANCE_DISABLED";
      g_governance_entry_blocked = false;
      return;
   }

   const int category = ClassifyGovernanceSkipCategory(skip_reason);
   const bool inference_ready = row_ready;
   const int argmax_class = inference_ready ? ResolveArgmaxClass(p_short, p_flat, p_long) : -1;
   const double normalized_entropy = inference_ready ? ComputeNormalizedSignalEntropy(p_short, p_flat, p_long) : EMPTY_VALUE;
   const double normalized_max_probability = inference_ready ? ComputeNormalizedMaxProbability(p_short, p_flat, p_long) : EMPTY_VALUE;
   const bool extreme_confidence = (inference_ready &&
      IsUsableValue(normalized_max_probability) &&
      normalized_max_probability >= InpGovernanceExtremeConfidenceThreshold);
   const bool signal_present = (inference_ready && decision != 0);
   const bool overlay_active = (signal_present && planned_risk_context != "" && planned_risk_context != "BASE");

   g_governance_current_skip_category = GovernanceSkipCategoryToString(category);
   g_governance_current_argmax_class = ArgmaxClassToString(argmax_class);
   g_governance_current_signal_entropy = normalized_entropy;
   g_governance_current_max_probability = normalized_max_probability;
   g_governance_current_extreme_confidence = extreme_confidence;

   const int slot = g_governance_window_slot;
   g_governance_skip_category_window[slot] = category;
   g_governance_inference_ready_window[slot] = inference_ready ? 1 : 0;
   g_governance_argmax_window[slot] = argmax_class;
   g_governance_extreme_confidence_window[slot] = extreme_confidence ? 1 : 0;
   g_governance_entropy_window[slot] = normalized_entropy;
   g_governance_signal_window[slot] = signal_present ? 1 : 0;
   g_governance_overlay_window[slot] = overlay_active ? 1 : 0;

   g_governance_window_slot++;
   if(g_governance_window_slot >= InpGovernanceWindowBars)
      g_governance_window_slot = 0;
   if(g_governance_window_count < InpGovernanceWindowBars)
      g_governance_window_count++;

   if(IsOperationalGovernanceSkipCategory(category))
      g_governance_consecutive_operational_skips++;
   else
      g_governance_consecutive_operational_skips = 0;

   int operational_skips = 0;
   int external_skips = 0;
   int feature_skips = 0;
   int warmup_skips = 0;
   int inference_samples = 0;
   int short_argmax = 0;
   int flat_argmax = 0;
   int long_argmax = 0;
   int extreme_confidence_count = 0;
   double entropy_sum = 0.0;
   int signal_samples = 0;
   int overlay_samples = 0;
   for(int i = 0; i < g_governance_window_count; i++)
   {
      const int window_category = g_governance_skip_category_window[i];
      if(IsOperationalGovernanceSkipCategory(window_category))
         operational_skips++;
      if(window_category == OP_GOV_SKIP_EXTERNAL)
         external_skips++;
      if(window_category == OP_GOV_SKIP_FEATURE)
         feature_skips++;
      if(window_category == OP_GOV_SKIP_WARMUP)
         warmup_skips++;

      if(g_governance_inference_ready_window[i] == 0)
         continue;

      inference_samples++;
      const int window_argmax_class = g_governance_argmax_window[i];
      if(window_argmax_class == 0)
         short_argmax++;
      else if(window_argmax_class == 1)
         flat_argmax++;
      else if(window_argmax_class == 2)
         long_argmax++;

      if(g_governance_extreme_confidence_window[i] != 0)
         extreme_confidence_count++;
      if(IsUsableValue(g_governance_entropy_window[i]))
         entropy_sum += g_governance_entropy_window[i];

      if(g_governance_signal_window[i] != 0)
      {
         signal_samples++;
         if(g_governance_overlay_window[i] != 0)
            overlay_samples++;
      }
   }

   g_governance_window_samples = g_governance_window_count;
   g_governance_inference_samples = inference_samples;
   g_governance_signal_samples = signal_samples;
   g_governance_operational_skip_rate = (g_governance_window_count > 0)
      ? ((double)operational_skips / (double)g_governance_window_count)
      : 0.0;
   g_governance_external_skip_rate = (g_governance_window_count > 0)
      ? ((double)external_skips / (double)g_governance_window_count)
      : 0.0;
   g_governance_feature_skip_rate = (g_governance_window_count > 0)
      ? ((double)feature_skips / (double)g_governance_window_count)
      : 0.0;
   g_governance_warmup_skip_rate = (g_governance_window_count > 0)
      ? ((double)warmup_skips / (double)g_governance_window_count)
      : 0.0;
   if(inference_samples > 0)
   {
      g_governance_max_argmax_class_share = MathMax((double)short_argmax, MathMax((double)flat_argmax, (double)long_argmax)) / (double)inference_samples;
      g_governance_extreme_confidence_rate = (double)extreme_confidence_count / (double)inference_samples;
      g_governance_avg_signal_entropy = entropy_sum / (double)inference_samples;
   }
   else
   {
      g_governance_max_argmax_class_share = 0.0;
      g_governance_extreme_confidence_rate = 0.0;
      g_governance_avg_signal_entropy = EMPTY_VALUE;
   }
   g_governance_risk_overlay_rate = (signal_samples > 0)
      ? ((double)overlay_samples / (double)signal_samples)
      : EMPTY_VALUE;

   if(g_governance_window_count < InpGovernanceMinSamples)
   {
      g_governance_state = "WARMING_UP";
      g_governance_reason = StringFormat("INSUFFICIENT_SAMPLES_%d_OF_%d", g_governance_window_count, InpGovernanceMinSamples);
      g_governance_entry_blocked = false;
      return;
   }

   string breach_tags = "";
   if(g_governance_operational_skip_rate > InpGovernanceMaxOperationalSkipRate)
      AppendGovernanceReasonTag(breach_tags, "OP_SKIP_RATE");
   if(g_governance_external_skip_rate > InpGovernanceMaxExternalSkipRate)
      AppendGovernanceReasonTag(breach_tags, "EXTERNAL_SKIP_RATE");
   if(g_governance_feature_skip_rate > InpGovernanceMaxFeatureSkipRate)
      AppendGovernanceReasonTag(breach_tags, "FEATURE_SKIP_RATE");
   if(g_governance_consecutive_operational_skips > InpGovernanceMaxConsecutiveOperationalSkips)
      AppendGovernanceReasonTag(breach_tags, "CONSECUTIVE_SKIPS");
   if(inference_samples > 0)
   {
      if(g_governance_max_argmax_class_share > InpGovernanceMaxArgmaxClassShare)
         AppendGovernanceReasonTag(breach_tags, "ARGMAX_DOMINANCE");
      if(g_governance_extreme_confidence_rate > InpGovernanceMaxExtremeConfidenceRate)
         AppendGovernanceReasonTag(breach_tags, "EXTREME_CONFIDENCE");
      if(IsUsableValue(g_governance_avg_signal_entropy) && g_governance_avg_signal_entropy < InpGovernanceMinNormalizedEntropy)
         AppendGovernanceReasonTag(breach_tags, "LOW_ENTROPY");
   }

   if(StringLen(breach_tags) <= 0)
   {
      g_governance_state = "OK";
      g_governance_reason = "WITHIN_LIMITS";
      g_governance_entry_blocked = false;
      return;
   }

   g_governance_reason = breach_tags;
   g_governance_entry_blocked = InpGovernanceBlockNewEntries;
   g_governance_state = g_governance_entry_blocked ? "BLOCKED" : "ALERT";
}

bool EnsureFolderPath(const string file_path, const bool use_common_files)
{
   int last_sep = -1;
   for(int i = 0; i < StringLen(file_path); i++)
   {
      ushort ch = StringGetCharacter(file_path, i);
      if(ch == '\\' || ch == '/')
         last_sep = i;
   }

   if(last_sep <= 0)
      return true;

   string folder_path = StringSubstr(file_path, 0, last_sep);
   if(folder_path == "")
      return true;

   if(use_common_files)
      return FolderCreate(folder_path, FILE_COMMON);
   return FolderCreate(folder_path);
}

bool EnsureLogHeader()
{
   if(!InpWriteCsvLog)
      return true;
   if(g_log_header_written)
      return true;

   EnsureFolderPath(InpCsvLogPath, InpLogUseCommonFiles);

   int read_flags = FILE_READ | FILE_TXT | FILE_ANSI;
   if(InpLogUseCommonFiles)
      read_flags |= FILE_COMMON;

   int read_handle = FileOpen(InpCsvLogPath, read_flags);
   if(read_handle != INVALID_HANDLE)
   {
      FileClose(read_handle);
      g_log_header_written = true;
      return true;
   }

   int write_flags = FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(InpLogUseCommonFiles)
      write_flags |= FILE_COMMON;

   int handle = FileOpen(InpCsvLogPath, write_flags);
   if(handle == INVALID_HANDLE)
   {
      Log(StringFormat("failed to create log file err=%d path=%s", GetLastError(), InpCsvLogPath));
      return false;
   }

   string header =
      "event_timestamp_gmt,bar_time_server,symbol,timeframe,feature_mode,feature_ready_count,row_ready,skip_reason,feature_checksum,"
      "p_short,p_flat,p_long,decision,decision_reason,cycle_tag,trade_action_reason,trade_fill_price,"
      "bid,ask,spread_points,balance,equity,margin,free_margin,floating_profit,managed_position_count,"
      "external_alignment_mode,external_relaxed_scope,external_fallback_used,external_fallback_count,external_fallback_details,model_path";
   FileWriteString(handle, header + "\r\n");
   FileClose(handle);
   g_log_header_written = true;
   return true;
}

bool EnsureTradeLedgerHeader()
{
   if(!InpWriteTradeLedger)
      return true;
   if(g_trade_ledger_header_written)
      return true;

   EnsureFolderPath(InpTradeLedgerPath, InpTradeLedgerUseCommonFiles);

   int read_flags = FILE_READ | FILE_TXT | FILE_ANSI;
   if(InpTradeLedgerUseCommonFiles)
      read_flags |= FILE_COMMON;

   int read_handle = FileOpen(InpTradeLedgerPath, read_flags);
   if(read_handle != INVALID_HANDLE)
   {
      FileClose(read_handle);
      g_trade_ledger_header_written = true;
      return true;
   }

   int write_flags = FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(InpTradeLedgerUseCommonFiles)
      write_flags |= FILE_COMMON;

   int handle = FileOpen(InpTradeLedgerPath, write_flags);
   if(handle == INVALID_HANDLE)
   {
      Log(StringFormat("failed to create trade ledger err=%d path=%s", GetLastError(), InpTradeLedgerPath));
      return false;
   }

   string header =
      "event_timestamp_gmt,symbol,position_ticket,position_identifier,direction,volume,entry_time_server,exit_time_server,"
      "entry_bar_time_server,exit_bar_time_server,entry_price,exit_price,hold_bars,close_reason,decision_at_entry,"
      "position_sizing_mode,stop_policy,risk_pct_multiplier_applied,risk_context,stop_atr_mult_applied,initial_stop_price,initial_stop_distance_points,initial_risk_amount,realized_r_multiple,"
      "gross_profit,swap,commission,fee,net_profit,max_floating_profit,min_floating_profit";
   FileWriteString(handle, header + "\r\n");
   FileClose(handle);
   g_trade_ledger_header_written = true;
   return true;
}

bool EnsureGovernanceLogHeader()
{
   if(!InpEnableGovernance || !InpWriteGovernanceLog)
      return true;
   if(g_governance_log_header_written)
      return true;

   EnsureFolderPath(InpGovernanceLogPath, InpGovernanceLogUseCommonFiles);

   int read_flags = FILE_READ | FILE_TXT | FILE_ANSI;
   if(InpGovernanceLogUseCommonFiles)
      read_flags |= FILE_COMMON;

   int read_handle = FileOpen(InpGovernanceLogPath, read_flags);
   if(read_handle != INVALID_HANDLE)
   {
      FileClose(read_handle);
      g_governance_log_header_written = true;
      return true;
   }

   int write_flags = FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(InpGovernanceLogUseCommonFiles)
      write_flags |= FILE_COMMON;

   int handle = FileOpen(InpGovernanceLogPath, write_flags);
   if(handle == INVALID_HANDLE)
   {
      Log(StringFormat("failed to create governance log err=%d path=%s", GetLastError(), InpGovernanceLogPath));
      return false;
   }

   string header =
      "event_timestamp_gmt,bar_time_server,symbol,timeframe,cycle_tag,row_ready,skip_reason,skip_category,decision,decision_reason,trade_action_reason,"
      "p_short,p_flat,p_long,argmax_class,signal_entropy_norm,max_probability,extreme_confidence,planned_risk_context,planned_risk_pct_multiplier,"
      "window_samples,inference_samples,signal_samples,operational_skip_rate,external_skip_rate,feature_skip_rate,warmup_skip_rate,max_argmax_class_share,"
      "extreme_confidence_rate,avg_signal_entropy_norm,risk_overlay_rate,consecutive_operational_skips,governance_state,governance_reason,entry_blocked_this_bar,"
      "external_alignment_mode,external_relaxed_scope,external_fallback_used,external_fallback_count,external_fallback_details";
   FileWriteString(handle, header + "\r\n");
   FileClose(handle);
   g_governance_log_header_written = true;
   return true;
}

void AppendShadowLog(
   const datetime bar_time_server,
   const string feature_mode,
   const int feature_ready_count,
   const bool row_ready,
   const string skip_reason,
   const ulong feature_checksum,
   const double p_short,
   const double p_flat,
   const double p_long,
   const string decision,
   const string decision_reason,
   const string cycle_tag,
   const string trade_action_reason,
   const double trade_fill_price
)
{
   if(!InpWriteCsvLog)
      return;
   if(!EnsureLogHeader())
      return;

   int flags = FILE_READ | FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(InpLogUseCommonFiles)
      flags |= FILE_COMMON;

   int handle = FileOpen(InpCsvLogPath, flags);
   if(handle == INVALID_HANDLE)
   {
      Log(StringFormat("failed to append log err=%d path=%s", GetLastError(), InpCsvLogPath));
      return;
   }

   FileSeek(handle, 0, SEEK_END);

   const double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   const double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   const double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   const double spread_points = (IsUsableValue(bid) && IsUsableValue(ask) && point > 0.0) ? ((ask - bid) / point) : EMPTY_VALUE;
   const double balance = AccountInfoDouble(ACCOUNT_BALANCE);
   const double equity = AccountInfoDouble(ACCOUNT_EQUITY);
   const double margin = AccountInfoDouble(ACCOUNT_MARGIN);
   const double free_margin = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
   const double floating_profit = AccountInfoDouble(ACCOUNT_PROFIT);
   const int managed_position_count = CountManagedPositions();

   string line =
      EscapeCsv(TimeToString(TimeGMT(), TIME_DATE | TIME_SECONDS)) + "," +
      EscapeCsv(TimeToString(bar_time_server, TIME_DATE | TIME_SECONDS)) + "," +
      EscapeCsv(_Symbol) + "," +
      EscapeCsv(EnumToString(_Period)) + "," +
      EscapeCsv(feature_mode) + "," +
      EscapeCsv((string)feature_ready_count) + "," +
      EscapeCsv(row_ready ? "true" : "false") + "," +
      EscapeCsv(skip_reason) + "," +
      EscapeCsv((string)feature_checksum) + "," +
      EscapeCsv(DoubleToString(p_short, 6)) + "," +
      EscapeCsv(DoubleToString(p_flat, 6)) + "," +
      EscapeCsv(DoubleToString(p_long, 6)) + "," +
      EscapeCsv(decision) + "," +
      EscapeCsv(decision_reason) + "," +
      EscapeCsv(cycle_tag) + "," +
      EscapeCsv(trade_action_reason) + "," +
      EscapeCsv(CsvDouble(trade_fill_price, 5)) + "," +
      EscapeCsv(CsvDouble(bid, 5)) + "," +
      EscapeCsv(CsvDouble(ask, 5)) + "," +
      EscapeCsv(CsvDouble(spread_points, 2)) + "," +
      EscapeCsv(CsvDouble(balance, 2)) + "," +
      EscapeCsv(CsvDouble(equity, 2)) + "," +
      EscapeCsv(CsvDouble(margin, 2)) + "," +
      EscapeCsv(CsvDouble(free_margin, 2)) + "," +
      EscapeCsv(CsvDouble(floating_profit, 2)) + "," +
      EscapeCsv(CsvInteger(managed_position_count)) + "," +
      EscapeCsv(g_effective_external_alignment_mode) + "," +
      EscapeCsv(g_effective_external_relaxed_scope) + "," +
      EscapeCsv(g_external_alignment_fallback_used ? "true" : "false") + "," +
      EscapeCsv(CsvInteger(g_external_alignment_fallback_count)) + "," +
      EscapeCsv(g_external_alignment_fallback_details) + "," +
      EscapeCsv(g_effective_onnx_model_path);

   FileWriteString(handle, line + "\r\n");
   FileClose(handle);
}

void AppendGovernanceLog(
   const datetime bar_time_server,
   const string cycle_tag,
   const bool row_ready,
   const string skip_reason,
   const string decision,
   const string decision_reason,
   const string trade_action_reason,
   const double p_short,
   const double p_flat,
   const double p_long,
   const bool entry_blocked_this_bar
)
{
   if(!InpEnableGovernance || !InpWriteGovernanceLog)
      return;
   if(!EnsureGovernanceLogHeader())
      return;

   int flags = FILE_READ | FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(InpGovernanceLogUseCommonFiles)
      flags |= FILE_COMMON;

   int handle = FileOpen(InpGovernanceLogPath, flags);
   if(handle == INVALID_HANDLE)
   {
      Log(StringFormat("failed to append governance log err=%d path=%s", GetLastError(), InpGovernanceLogPath));
      return;
   }

   FileSeek(handle, 0, SEEK_END);

   string line =
      EscapeCsv(TimeToString(TimeGMT(), TIME_DATE | TIME_SECONDS)) + "," +
      EscapeCsv(TimeToString(bar_time_server, TIME_DATE | TIME_SECONDS)) + "," +
      EscapeCsv(_Symbol) + "," +
      EscapeCsv(EnumToString(_Period)) + "," +
      EscapeCsv(cycle_tag) + "," +
      EscapeCsv(row_ready ? "true" : "false") + "," +
      EscapeCsv(skip_reason) + "," +
      EscapeCsv(g_governance_current_skip_category) + "," +
      EscapeCsv(decision) + "," +
      EscapeCsv(decision_reason) + "," +
      EscapeCsv(trade_action_reason) + "," +
      EscapeCsv(CsvDouble(p_short, 6)) + "," +
      EscapeCsv(CsvDouble(p_flat, 6)) + "," +
      EscapeCsv(CsvDouble(p_long, 6)) + "," +
      EscapeCsv(g_governance_current_argmax_class) + "," +
      EscapeCsv(CsvDouble(g_governance_current_signal_entropy, 6)) + "," +
      EscapeCsv(CsvDouble(g_governance_current_max_probability, 6)) + "," +
      EscapeCsv(g_governance_current_extreme_confidence ? "true" : "false") + "," +
      EscapeCsv(g_governance_current_risk_context) + "," +
      EscapeCsv(CsvDouble(g_governance_current_risk_pct_multiplier, 4)) + "," +
      EscapeCsv(CsvInteger(g_governance_window_samples)) + "," +
      EscapeCsv(CsvInteger(g_governance_inference_samples)) + "," +
      EscapeCsv(CsvInteger(g_governance_signal_samples)) + "," +
      EscapeCsv(CsvDouble(g_governance_operational_skip_rate, 6)) + "," +
      EscapeCsv(CsvDouble(g_governance_external_skip_rate, 6)) + "," +
      EscapeCsv(CsvDouble(g_governance_feature_skip_rate, 6)) + "," +
      EscapeCsv(CsvDouble(g_governance_warmup_skip_rate, 6)) + "," +
      EscapeCsv(CsvDouble(g_governance_max_argmax_class_share, 6)) + "," +
      EscapeCsv(CsvDouble(g_governance_extreme_confidence_rate, 6)) + "," +
      EscapeCsv(CsvDouble(g_governance_avg_signal_entropy, 6)) + "," +
      EscapeCsv(CsvDouble(g_governance_risk_overlay_rate, 6)) + "," +
      EscapeCsv(CsvInteger(g_governance_consecutive_operational_skips)) + "," +
      EscapeCsv(g_governance_state) + "," +
      EscapeCsv(g_governance_reason) + "," +
      EscapeCsv(entry_blocked_this_bar ? "true" : "false") + "," +
      EscapeCsv(g_effective_external_alignment_mode) + "," +
      EscapeCsv(g_effective_external_relaxed_scope) + "," +
      EscapeCsv(g_external_alignment_fallback_used ? "true" : "false") + "," +
      EscapeCsv(CsvInteger(g_external_alignment_fallback_count)) + "," +
      EscapeCsv(g_external_alignment_fallback_details);

   FileWriteString(handle, line + "\r\n");
   FileClose(handle);
}

ulong ComputeFeatureChecksum(const double &features[])
{
   ulong hash = 2166136261;
   const int feature_count = ArraySize(features);

   for(int i = 0; i < feature_count; i++)
   {
      string token = DoubleToString(features[i], 8) + "|";
      const int token_len = StringLen(token);
      for(int j = 0; j < token_len; j++)
      {
         hash ^= (ulong)StringGetCharacter(token, j);
         hash *= 16777619;
      }
   }

   return hash;
}

bool IsUsableValue(const double value)
{
   return (MathIsValidNumber(value) && MathAbs(value) < (EMPTY_VALUE / 2.0));
}

double SafeDivideValue(const double numerator, const double denominator)
{
   if(denominator == 0.0)
      return EMPTY_VALUE;
   return numerator / denominator;
}

bool CopyIndicatorBufferWindow(
   const int handle,
   const int buffer_index,
   const int start_shift,
   const int count,
   double &values[],
   const string label,
   string &skip_reason
)
{
   if(handle == INVALID_HANDLE)
   {
      skip_reason = "HANDLE_INVALID_" + label;
      return false;
   }

   ResetLastError();
   const int bars_calculated = BarsCalculated(handle);
   if(bars_calculated < (start_shift + count))
   {
      skip_reason = StringFormat("HANDLE_NOT_READY_%s_%d", label, bars_calculated);
      return false;
   }

   ArraySetAsSeries(values, false);
   const int copied = CopyBuffer(handle, buffer_index, start_shift, count, values);
   if(copied < count)
   {
      skip_reason = StringFormat("COPYBUFFER_FAIL_%s_%d_ERR_%d", label, copied, GetLastError());
      return false;
   }

   for(int i = 0; i < count; i++)
   {
      if(!IsUsableValue(values[i]))
      {
         skip_reason = StringFormat("INDICATOR_INVALID_%s_%d", label, i);
         return false;
      }
   }

   return true;
}

datetime BuildDateTimeValue(
   const int year,
   const int month,
   const int day,
   const int hour,
   const int minute,
   const int second
)
{
   MqlDateTime dt;
   ZeroMemory(dt);
   dt.year = year;
   dt.mon = month;
   dt.day = day;
   dt.hour = hour;
   dt.min = minute;
   dt.sec = second;
   return StructToTime(dt);
}

int NthWeekdayOfMonth(const int year, const int month, const int weekday, const int occurrence)
{
   MqlDateTime first_day;
   ZeroMemory(first_day);
   first_day.year = year;
   first_day.mon = month;
   first_day.day = 1;
   datetime first_timestamp = StructToTime(first_day);
   TimeToStruct(first_timestamp, first_day);
   const int delta = (weekday - first_day.day_of_week + 7) % 7;
   return 1 + delta + ((occurrence - 1) * 7);
}

bool IsNewYorkDstUtc(const datetime timestamp_utc)
{
   MqlDateTime utc_struct;
   TimeToStruct(timestamp_utc, utc_struct);
   const int second_sunday_march = NthWeekdayOfMonth(utc_struct.year, 3, 0, 2);
   const int first_sunday_november = NthWeekdayOfMonth(utc_struct.year, 11, 0, 1);
   const datetime dst_start_utc = BuildDateTimeValue(utc_struct.year, 3, second_sunday_march, 7, 0, 0);
   const datetime dst_end_utc = BuildDateTimeValue(utc_struct.year, 11, first_sunday_november, 6, 0, 0);
   return (timestamp_utc >= dst_start_utc && timestamp_utc < dst_end_utc);
}

datetime ConvertUtcToNewYork(const datetime timestamp_utc)
{
   const int offset_seconds = IsNewYorkDstUtc(timestamp_utc) ? (-4 * 3600) : (-5 * 3600);
   return timestamp_utc + offset_seconds;
}

int BuildNyDateKeyFromUtc(const datetime timestamp_utc)
{
   MqlDateTime ny_struct;
   TimeToStruct(ConvertUtcToNewYork(timestamp_utc), ny_struct);
   return (ny_struct.year * 10000) + (ny_struct.mon * 100) + ny_struct.day;
}

bool ComputeSessionFeatureValues(
   const MqlRates &rates[],
   const int total_bars,
   const int current_index,
   double &value_overnight_return,
   double &value_is_us_cash_open,
   double &value_minutes_from_cash_open,
   double &value_is_first_30m_after_open,
   double &value_is_last_30m_before_cash_close,
   string &skip_reason
)
{
   const datetime current_close_utc = rates[current_index].time + PeriodSeconds(PERIOD_M5);
   MqlDateTime close_ny_struct;
   TimeToStruct(ConvertUtcToNewYork(current_close_utc), close_ny_struct);

   const int current_ny_date_key = (close_ny_struct.year * 10000) + (close_ny_struct.mon * 100) + close_ny_struct.day;
   const int close_minutes = (close_ny_struct.hour * 60) + close_ny_struct.min;
   const int minutes_from_open = close_minutes - (9 * 60 + 30);
   const int minutes_to_close = (16 * 60) - close_minutes;

   value_is_us_cash_open = ((minutes_from_open > 0) && (minutes_to_close >= 0)) ? 1.0 : 0.0;
   value_minutes_from_cash_open = (double)minutes_from_open;
   value_is_first_30m_after_open = ((minutes_from_open > 0) && (minutes_from_open <= 30)) ? 1.0 : 0.0;
   value_is_last_30m_before_cash_close = ((minutes_to_close > 0) && (minutes_to_close <= 30)) ? 1.0 : 0.0;

   double cash_open_today = EMPTY_VALUE;
   double prev_cash_close = EMPTY_VALUE;

   for(int i = 0; i < total_bars; i++)
   {
      const datetime bar_open_utc = rates[i].time;
      const datetime bar_close_utc = rates[i].time + PeriodSeconds(PERIOD_M5);

      MqlDateTime open_ny_struct;
      MqlDateTime bar_close_ny_struct;
      TimeToStruct(ConvertUtcToNewYork(bar_open_utc), open_ny_struct);
      TimeToStruct(ConvertUtcToNewYork(bar_close_utc), bar_close_ny_struct);

      const int open_ny_date_key = (open_ny_struct.year * 10000) + (open_ny_struct.mon * 100) + open_ny_struct.day;
      const int close_ny_date_key = (bar_close_ny_struct.year * 10000) + (bar_close_ny_struct.mon * 100) + bar_close_ny_struct.day;
      const int open_minutes = (open_ny_struct.hour * 60) + open_ny_struct.min;
      const int bar_close_minutes = (bar_close_ny_struct.hour * 60) + bar_close_ny_struct.min;

      if(open_ny_date_key == current_ny_date_key && open_minutes == (9 * 60 + 30) && !IsUsableValue(cash_open_today))
         cash_open_today = rates[i].open;

      if(close_ny_date_key < current_ny_date_key && bar_close_minutes == (16 * 60) && rates[i].close > 0.0)
         prev_cash_close = rates[i].close;
   }

   if(!IsUsableValue(cash_open_today))
   {
      skip_reason = "SESSION_CASH_OPEN_NOT_FOUND";
      return false;
   }

   if(!IsUsableValue(prev_cash_close))
   {
      skip_reason = "SESSION_PREV_CASH_CLOSE_NOT_FOUND";
      return false;
   }

   value_overnight_return = SafeDivideValue(cash_open_today, prev_cash_close) - 1.0;
   if(!IsUsableValue(value_overnight_return))
   {
      skip_reason = "SESSION_OVERNIGHT_INVALID";
      return false;
   }

   return true;
}

double RollingMeanSlice(const double &values[], const int start_index, const int window)
{
   if(window <= 0)
      return EMPTY_VALUE;

   double sum = 0.0;
   for(int i = 0; i < window; i++)
   {
      const double value = values[start_index + i];
      if(!IsUsableValue(value))
         return EMPTY_VALUE;
      sum += value;
   }
   return sum / window;
}

double RollingSumSlice(const double &values[], const int start_index, const int window)
{
   if(window <= 0)
      return EMPTY_VALUE;

   double sum = 0.0;
   for(int i = 0; i < window; i++)
   {
      const double value = values[start_index + i];
      if(!IsUsableValue(value))
         return EMPTY_VALUE;
      sum += value;
   }
   return sum;
}

double RollingMinSlice(const double &values[], const int start_index, const int window)
{
   if(window <= 0)
      return EMPTY_VALUE;

   double out = DBL_MAX;
   for(int i = 0; i < window; i++)
   {
      const double value = values[start_index + i];
      if(!IsUsableValue(value))
         return EMPTY_VALUE;
      if(value < out)
         out = value;
   }
   return out;
}

double RollingMaxSlice(const double &values[], const int start_index, const int window)
{
   if(window <= 0)
      return EMPTY_VALUE;

   double out = -DBL_MAX;
   for(int i = 0; i < window; i++)
   {
      const double value = values[start_index + i];
      if(!IsUsableValue(value))
         return EMPTY_VALUE;
      if(value > out)
         out = value;
   }
   return out;
}

bool ComputeEmaSeries(const double &values[], const int total_count, const int period, double &out[])
{
   ArrayResize(out, total_count);
   for(int i = 0; i < total_count; i++)
      out[i] = EMPTY_VALUE;

   int first_valid = -1;
   for(int i = 0; i < total_count; i++)
   {
      if(IsUsableValue(values[i]))
      {
         first_valid = i;
         out[i] = values[i];
         break;
      }
   }
   if(first_valid < 0)
      return false;

   const double alpha = 2.0 / (period + 1.0);
   for(int i = first_valid + 1; i < total_count; i++)
   {
      if(!IsUsableValue(values[i]) || !IsUsableValue(out[i - 1]))
      {
         out[i] = EMPTY_VALUE;
         continue;
      }
      out[i] = (alpha * values[i]) + ((1.0 - alpha) * out[i - 1]);
   }

   const int valid_start = first_valid + period - 1;
   for(int i = first_valid; i < total_count && i < valid_start; i++)
      out[i] = EMPTY_VALUE;

   return true;
}

bool ComputeTrueRangeSeries(const MqlRates &rates[], const int total_count, double &out[])
{
   ArrayResize(out, total_count);
   for(int i = 0; i < total_count; i++)
   {
      const double high_low = rates[i].high - rates[i].low;
      if(i == 0)
      {
         out[i] = high_low;
         continue;
      }

      const double high_prev_close = MathAbs(rates[i].high - rates[i - 1].close);
      const double low_prev_close = MathAbs(rates[i].low - rates[i - 1].close);
      out[i] = MathMax(high_low, MathMax(high_prev_close, low_prev_close));
   }
   return true;
}

bool ComputeWilderSmoothSeries(const double &values[], const int total_count, const int period, double &out[])
{
   ArrayResize(out, total_count);
   for(int i = 0; i < total_count; i++)
      out[i] = EMPTY_VALUE;

   int first_end = -1;
   for(int end_index = period - 1; end_index < total_count; end_index++)
   {
      const int start_index = end_index - period + 1;
      double sum = 0.0;
      bool window_ok = true;
      for(int i = start_index; i <= end_index; i++)
      {
         if(!IsUsableValue(values[i]))
         {
            window_ok = false;
            break;
         }
         sum += values[i];
      }

      if(window_ok)
      {
         first_end = end_index;
         out[end_index] = sum / period;
         break;
      }
   }

   if(first_end < 0)
      return false;

   for(int i = first_end + 1; i < total_count; i++)
   {
      if(!IsUsableValue(values[i]) || !IsUsableValue(out[i - 1]))
      {
         out[i] = EMPTY_VALUE;
         continue;
      }
      out[i] = ((out[i - 1] * (period - 1)) + values[i]) / period;
   }
   return true;
}

bool LoadExternalSymbolRatesAligned(
   const string symbol,
   const int bars_needed,
   const datetime target_close_utc,
   MqlRates &rates[],
   string &skip_reason
)
{
   if(!SymbolSelect(symbol, true))
   {
      skip_reason = "EXTERNAL_SYMBOL_SELECT_FAIL_" + symbol;
      return false;
   }

   ArraySetAsSeries(rates, false);
   ResetLastError();
   const int period_seconds = PeriodSeconds(PERIOD_M5);
   const datetime target_bar_open_utc = target_close_utc - period_seconds;
   int target_shift = iBarShift(symbol, PERIOD_M5, target_bar_open_utc, true);
   bool using_stale_fallback = false;
   if(target_shift < 0)
   {
      if(!AllowExternalStaleFallback(symbol))
      {
         skip_reason = "EXTERNAL_TIMESTAMP_MISMATCH_" + symbol;
         return false;
      }

      target_shift = iBarShift(symbol, PERIOD_M5, target_bar_open_utc, false);
      if(target_shift < 0)
      {
         skip_reason = "EXTERNAL_TIMESTAMP_MISMATCH_" + symbol;
         return false;
      }
      using_stale_fallback = true;
   }

   const int copied = CopyRates(symbol, PERIOD_M5, target_shift, bars_needed, rates);
   if(copied != bars_needed)
   {
      skip_reason = StringFormat("EXTERNAL_RATES_NOT_READY_%s_%d_OF_%d_ERR_%d", symbol, copied, bars_needed, GetLastError());
      return false;
   }

   const int total_bars = ArraySize(rates);
   const datetime latest_close_utc = rates[total_bars - 1].time + PeriodSeconds(PERIOD_M5);
   if(latest_close_utc != target_close_utc)
   {
      if(!using_stale_fallback ||
         latest_close_utc <= 0 ||
         latest_close_utc > target_close_utc ||
         !SameUtcCalendarDate(latest_close_utc, target_close_utc))
      {
         skip_reason = StringFormat("EXTERNAL_TIMESTAMP_MISMATCH_%s", symbol);
         return false;
      }

      const int stale_bars = (int)((target_close_utc - latest_close_utc) / period_seconds);
      if(stale_bars <= 0 || stale_bars > g_effective_external_max_stale_bars)
      {
         skip_reason = StringFormat("EXTERNAL_TIMESTAMP_MISMATCH_%s", symbol);
         return false;
      }

      RecordExternalAlignmentFallback(symbol, stale_bars);
   }

   return true;
}

bool LoadClosedRates(const int bars_needed, MqlRates &rates[], string &skip_reason)
{
   ArraySetAsSeries(rates, false);
   ResetLastError();
   const int copied = CopyRates(_Symbol, PERIOD_M5, 1, bars_needed, rates);
   if(copied < bars_needed)
   {
      skip_reason = StringFormat("RATES_NOT_READY_%d_OF_%d_ERR_%d", copied, bars_needed, GetLastError());
      return false;
   }
   return true;
}

double PopulationStdSlice(const double &values[], const int start_index, const int window)
{
   if(window <= 0)
      return EMPTY_VALUE;

   double sum = 0.0;
   for(int i = 0; i < window; i++)
   {
      const double value = values[start_index + i];
      if(!IsUsableValue(value))
         return EMPTY_VALUE;
      sum += value;
   }

   const double mean = sum / window;
   double sq_sum = 0.0;
   for(int i = 0; i < window; i++)
   {
      const double diff = values[start_index + i] - mean;
      sq_sum += diff * diff;
   }

   return MathSqrt(sq_sum / window);
}

double RollingZscoreCurrent(const double &values[], const int total_count, const int window)
{
   if(total_count < window || window <= 0)
      return EMPTY_VALUE;

   const int start_index = total_count - window;
   double sum = 0.0;
   for(int i = start_index; i < total_count; i++)
   {
      if(!IsUsableValue(values[i]))
         return EMPTY_VALUE;
      sum += values[i];
   }

   const double mean = sum / window;
   const double std = PopulationStdSlice(values, start_index, window);
   if(!IsUsableValue(std))
      return EMPTY_VALUE;
   if(std == 0.0)
      return 0.0;

   return (values[total_count - 1] - mean) / std;
}

bool BuildPriceCorePartialFeatures(
   double &features[],
   int &feature_ready_count,
   bool &feature_vector_complete,
   string &skip_reason
)
{
   const int bars_needed = MathMax(InpWarmupBars, 1000);
   MqlRates rates[];
   if(!LoadClosedRates(bars_needed, rates, skip_reason))
      return false;

   const int total_bars = ArraySize(rates);
   if(total_bars < 60)
   {
      skip_reason = StringFormat("PRICE_CORE_WARMUP_%d", total_bars);
      return false;
   }

   double close_values[];
   double log_return_1_series[];
   double hl_range_series[];
   ArrayResize(close_values, total_bars);
   ArrayResize(log_return_1_series, total_bars);
   ArrayResize(hl_range_series, total_bars);

   for(int i = 0; i < total_bars; i++)
   {
      close_values[i] = rates[i].close;
      log_return_1_series[i] = EMPTY_VALUE;
      hl_range_series[i] = EMPTY_VALUE;
   }

   for(int i = 1; i < total_bars; i++)
   {
      if(rates[i - 1].close > 0.0 && rates[i].close > 0.0)
         log_return_1_series[i] = MathLog(rates[i].close / rates[i - 1].close);
   }

   for(int i = 0; i < total_bars; i++)
   {
      hl_range_series[i] = SafeDivideValue(rates[i].high - rates[i].low, rates[i].close);
   }

   const int t = total_bars - 1;
   const double value_log_return_1 = log_return_1_series[t];
   const double value_log_return_3 = (rates[t - 3].close > 0.0 && rates[t].close > 0.0) ? MathLog(rates[t].close / rates[t - 3].close) : EMPTY_VALUE;
   const double value_hl_range = hl_range_series[t];
   const double value_close_open_ratio = SafeDivideValue(rates[t].close, rates[t].open);
   const double value_gap_percent = SafeDivideValue(rates[t].open, rates[t - 1].close) - 1.0;
   const double value_close_prev_close_ratio = SafeDivideValue(rates[t].close, rates[t - 1].close);
   const double value_us100_simple_return_1 = SafeDivideValue(rates[t].close, rates[t - 1].close) - 1.0;
   const double value_return_zscore_20 = RollingZscoreCurrent(log_return_1_series, total_bars, 20);
   const double value_hl_zscore_50 = RollingZscoreCurrent(hl_range_series, total_bars, 50);
   const double value_roc_12 = SafeDivideValue(rates[t].close, rates[t - 12].close) - 1.0;

   const double hv20_std = PopulationStdSlice(log_return_1_series, total_bars - 20, 20);
   const double hv5_std = PopulationStdSlice(log_return_1_series, total_bars - 5, 5);
   const double value_historical_vol_20 = IsUsableValue(hv20_std) ? (hv20_std * MathSqrt(OP_BARS_PER_YEAR_5M)) : EMPTY_VALUE;
   const double value_historical_vol_5_over_20 = SafeDivideValue(
      IsUsableValue(hv5_std) ? (hv5_std * MathSqrt(OP_BARS_PER_YEAR_5M)) : EMPTY_VALUE,
      value_historical_vol_20
   );

   double ema9_current[];
   double ema20_series[];
   double ema50_series[];
   double ema200_current[];
   double sma50_current[];
   double sma200_current[];
   double rsi14_window[];
   double rsi50_current[];
   double stoch_k_current[];
   double stoch_d_current[];
   double atr14_current[];
   double atr20_current[];
   double atr50_current[];
   double bb_mid_current[];
   double bb_upper_current[];
   double bb_lower_current[];
   double adx_current[];
   double plus_di_current[];
   double minus_di_current[];

   if(!CopyIndicatorBufferWindow(g_handle_ema9, 0, 1, 1, ema9_current, "EMA9", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_ema20, 0, 1, 50, ema20_series, "EMA20", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_ema50, 0, 1, 50, ema50_series, "EMA50", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_ema200, 0, 1, 1, ema200_current, "EMA200", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_sma50, 0, 1, 1, sma50_current, "SMA50", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_sma200, 0, 1, 1, sma200_current, "SMA200", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_rsi14, 0, 1, 18, rsi14_window, "RSI14", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_rsi50, 0, 1, 1, rsi50_current, "RSI50", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_stoch14, 0, 1, 1, stoch_k_current, "STOCH_MAIN", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_stoch14, 1, 1, 1, stoch_d_current, "STOCH_SIGNAL", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_atr14, 0, 1, 1, atr14_current, "ATR14", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_atr20, 0, 1, 1, atr20_current, "ATR20", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_atr50, 0, 1, 1, atr50_current, "ATR50", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_bands20, 0, 1, 1, bb_mid_current, "BB_MID", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_bands20, 1, 1, 1, bb_upper_current, "BB_UPPER", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_bands20, 2, 1, 1, bb_lower_current, "BB_LOWER", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_adx14, 0, 1, 1, adx_current, "ADX14", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_adx14, 1, 1, 1, plus_di_current, "PLUS_DI14", skip_reason))
      return false;
   if(!CopyIndicatorBufferWindow(g_handle_adx14, 2, 1, 1, minus_di_current, "MINUS_DI14", skip_reason))
      return false;

   double ema20_ema50_diff_series[];
   ArrayResize(ema20_ema50_diff_series, 50);
   for(int i = 0; i < 50; i++)
      ema20_ema50_diff_series[i] = ema20_series[i] - ema50_series[i];

   const double value_atr_14 = atr14_current[0];
   const double value_atr_20 = atr20_current[0];
   const double value_atr_50 = atr50_current[0];
   const double value_return_1_over_atr_14 = SafeDivideValue(
      value_us100_simple_return_1,
      SafeDivideValue(value_atr_14, rates[t].close)
   );
   const double value_close_ema20_ratio = SafeDivideValue(rates[t].close, ema20_series[49]);
   const double value_close_ema50_ratio = SafeDivideValue(rates[t].close, ema50_series[49]);
   const double value_ema9_ema20_diff = ema9_current[0] - ema20_series[49];
   const double value_ema20_ema50_diff = ema20_series[49] - ema50_series[49];
   const double value_ema50_ema200_diff = ema50_series[49] - ema200_current[0];
   const double value_ema20_ema50_spread_zscore_50 = RollingZscoreCurrent(ema20_ema50_diff_series, 50, 50);
   const double value_sma50_sma200_ratio = SafeDivideValue(sma50_current[0], sma200_current[0]);
   const double value_rsi_14 = rsi14_window[17];
   const double value_rsi_50 = rsi50_current[0];
   const double value_rsi_14_slope_3 = (rsi14_window[17] - rsi14_window[14]) / 3.0;
   const double value_rsi_14_minus_50 = rsi14_window[17] - 50.0;
   const double value_stoch_kd_diff = stoch_k_current[0] - stoch_d_current[0];
   const double value_atr_14_over_atr_50 = SafeDivideValue(value_atr_14, value_atr_50);
   const double value_bollinger_width_20 = SafeDivideValue(bb_upper_current[0] - bb_lower_current[0], bb_mid_current[0]);
   const double value_bb_position_20 = SafeDivideValue(rates[t].close - bb_lower_current[0], bb_upper_current[0] - bb_lower_current[0]);
   const double kc_mid_20 = ema20_series[49];
   const double kc_upper = kc_mid_20 + (1.5 * value_atr_20);
   const double kc_lower = kc_mid_20 - (1.5 * value_atr_20);
   const double value_bb_squeeze = ((bb_upper_current[0] <= kc_upper) && (bb_lower_current[0] >= kc_lower)) ? 1.0 : 0.0;
   const double value_adx_14 = adx_current[0];
   const double value_di_spread_14 = plus_di_current[0] - minus_di_current[0];
   double value_overnight_return = EMPTY_VALUE;
   double value_is_us_cash_open = EMPTY_VALUE;
   double value_minutes_from_cash_open = EMPTY_VALUE;
   double value_is_first_30m_after_open = EMPTY_VALUE;
   double value_is_last_30m_before_cash_close = EMPTY_VALUE;

   if(!ComputeSessionFeatureValues(
      rates,
      total_bars,
      t,
      value_overnight_return,
      value_is_us_cash_open,
      value_minutes_from_cash_open,
      value_is_first_30m_after_open,
      value_is_last_30m_before_cash_close,
      skip_reason
   ))
   {
      return false;
   }

   double value_stochrsi_kd_diff = EMPTY_VALUE;
   double value_ppo_hist_12_26_9 = EMPTY_VALUE;
   double value_trix_15 = EMPTY_VALUE;
   double value_supertrend_10_3 = EMPTY_VALUE;
   double value_vortex_indicator = EMPTY_VALUE;
   double value_vix_change_1 = EMPTY_VALUE;
   double value_vix_zscore_20 = EMPTY_VALUE;
   double value_us10yr_change_1 = EMPTY_VALUE;
   double value_us10yr_zscore_20 = EMPTY_VALUE;
   double value_usdx_change_1 = EMPTY_VALUE;
   double value_usdx_zscore_20 = EMPTY_VALUE;
   double value_nvda_xnas_log_return_1 = EMPTY_VALUE;
   double value_aapl_xnas_log_return_1 = EMPTY_VALUE;
   double value_msft_xnas_log_return_1 = EMPTY_VALUE;
   double value_amzn_xnas_log_return_1 = EMPTY_VALUE;
   double value_mega8_equal_return_1 = EMPTY_VALUE;
   double value_top3_weighted_return_1 = EMPTY_VALUE;
   double value_mega8_pos_breadth_1 = EMPTY_VALUE;
   double value_mega8_dispersion_5 = EMPTY_VALUE;
   double value_us100_minus_mega8_equal_return_1 = EMPTY_VALUE;
   double value_us100_minus_top3_weighted_return_1 = EMPTY_VALUE;

   const bool needs_custom_block =
      IsFeatureRequested("stochrsi_kd_diff") ||
      IsFeatureRequested("ppo_hist_12_26_9") ||
      IsFeatureRequested("trix_15") ||
      IsFeatureRequested("supertrend_10_3") ||
      IsFeatureRequested("vortex_indicator");

   if(needs_custom_block)
   {
      double stochrsi_raw_values[];
      double stochrsi_k_values[];
      ArrayResize(stochrsi_raw_values, 5);
      ArrayResize(stochrsi_k_values, 3);

      for(int i = 0; i < 5; i++)
      {
         const double rsi_low = RollingMinSlice(rsi14_window, i, 14);
         const double rsi_high = RollingMaxSlice(rsi14_window, i, 14);
         if(!IsUsableValue(rsi_low) || !IsUsableValue(rsi_high))
         {
            skip_reason = "CUSTOM_STOCHRSI_WINDOW_INVALID";
            return false;
         }
         stochrsi_raw_values[i] = SafeDivideValue((rsi14_window[i + 13] - rsi_low) * 100.0, rsi_high - rsi_low);
      }

      for(int i = 0; i < 3; i++)
         stochrsi_k_values[i] = RollingMeanSlice(stochrsi_raw_values, i, 3);

      const double stochrsi_d_current = RollingMeanSlice(stochrsi_k_values, 0, 3);
      value_stochrsi_kd_diff = stochrsi_k_values[2] - stochrsi_d_current;

      double ema12_series[];
      double ema26_series[];
      double ppo_series[];
      double ppo_signal_series[];
      if(!ComputeEmaSeries(close_values, total_bars, 12, ema12_series))
      {
         skip_reason = "CUSTOM_EMA12_FAIL";
         return false;
      }
      if(!ComputeEmaSeries(close_values, total_bars, 26, ema26_series))
      {
         skip_reason = "CUSTOM_EMA26_FAIL";
         return false;
      }

      ArrayResize(ppo_series, total_bars);
      for(int i = 0; i < total_bars; i++)
      {
         if(IsUsableValue(ema12_series[i]) && IsUsableValue(ema26_series[i]))
            ppo_series[i] = SafeDivideValue((ema12_series[i] - ema26_series[i]) * 100.0, ema26_series[i]);
         else
            ppo_series[i] = EMPTY_VALUE;
      }

      if(!ComputeEmaSeries(ppo_series, total_bars, 9, ppo_signal_series))
      {
         skip_reason = "CUSTOM_PPO_SIGNAL_FAIL";
         return false;
      }
      value_ppo_hist_12_26_9 = ppo_series[t] - ppo_signal_series[t];

      double trix_ema1[];
      double trix_ema2[];
      double trix_ema3[];
      if(!ComputeEmaSeries(close_values, total_bars, 15, trix_ema1))
      {
         skip_reason = "CUSTOM_TRIX_EMA1_FAIL";
         return false;
      }
      if(!ComputeEmaSeries(trix_ema1, total_bars, 15, trix_ema2))
      {
         skip_reason = "CUSTOM_TRIX_EMA2_FAIL";
         return false;
      }
      if(!ComputeEmaSeries(trix_ema2, total_bars, 15, trix_ema3))
      {
         skip_reason = "CUSTOM_TRIX_EMA3_FAIL";
         return false;
      }
      value_trix_15 = SafeDivideValue(trix_ema3[t], trix_ema3[t - 1]) - 1.0;

      double true_range_series[];
      if(!ComputeTrueRangeSeries(rates, total_bars, true_range_series))
      {
         skip_reason = "CUSTOM_TR_FAIL";
         return false;
      }

      double atr10_series[];
      if(!ComputeWilderSmoothSeries(true_range_series, total_bars, 10, atr10_series))
      {
         skip_reason = "CUSTOM_ATR10_FAIL";
         return false;
      }

      double supertrend_upper[];
      double supertrend_lower[];
      double supertrend_state[];
      double vm_plus_series[];
      double vm_minus_series[];
      ArrayResize(supertrend_upper, total_bars);
      ArrayResize(supertrend_lower, total_bars);
      ArrayResize(supertrend_state, total_bars);
      ArrayResize(vm_plus_series, total_bars);
      ArrayResize(vm_minus_series, total_bars);

      int first_supertrend_valid = -1;
      for(int i = 0; i < total_bars; i++)
      {
         supertrend_upper[i] = EMPTY_VALUE;
         supertrend_lower[i] = EMPTY_VALUE;
         supertrend_state[i] = EMPTY_VALUE;
         vm_plus_series[i] = EMPTY_VALUE;
         vm_minus_series[i] = EMPTY_VALUE;

         if(i == 0)
            continue;

         vm_plus_series[i] = MathAbs(rates[i].high - rates[i - 1].low);
         vm_minus_series[i] = MathAbs(rates[i].low - rates[i - 1].high);

         if(!IsUsableValue(atr10_series[i]))
            continue;

         const double hl2 = (rates[i].high + rates[i].low) / 2.0;
         const double basic_upper = hl2 + (3.0 * atr10_series[i]);
         const double basic_lower = hl2 - (3.0 * atr10_series[i]);
         if(first_supertrend_valid < 0)
         {
            first_supertrend_valid = i;
            supertrend_upper[i] = basic_upper;
            supertrend_lower[i] = basic_lower;
            supertrend_state[i] = (rates[i].close >= hl2) ? 1.0 : -1.0;
            continue;
         }

         const double prev_upper = supertrend_upper[i - 1];
         const double prev_lower = supertrend_lower[i - 1];
         const double prev_close = rates[i - 1].close;

         supertrend_upper[i] = (!IsUsableValue(prev_upper) || basic_upper < prev_upper || prev_close > prev_upper) ? basic_upper : prev_upper;
         supertrend_lower[i] = (!IsUsableValue(prev_lower) || basic_lower > prev_lower || prev_close < prev_lower) ? basic_lower : prev_lower;

         const double prev_state = supertrend_state[i - 1];
         if(prev_state == 1.0)
            supertrend_state[i] = (rates[i].close < supertrend_lower[i]) ? -1.0 : 1.0;
         else
            supertrend_state[i] = (rates[i].close > supertrend_upper[i]) ? 1.0 : -1.0;
      }

      value_supertrend_10_3 = supertrend_state[t];

      const double vortex_tr_sum = RollingSumSlice(true_range_series, total_bars - 14, 14);
      const double vortex_vm_plus_sum = RollingSumSlice(vm_plus_series, total_bars - 14, 14);
      const double vortex_vm_minus_sum = RollingSumSlice(vm_minus_series, total_bars - 14, 14);
      const double vortex_plus = SafeDivideValue(vortex_vm_plus_sum, vortex_tr_sum);
      const double vortex_minus = SafeDivideValue(vortex_vm_minus_sum, vortex_tr_sum);
      value_vortex_indicator = vortex_plus - vortex_minus;
   }

   const bool needs_external_block =
      IsFeatureRequested("vix_change_1") ||
      IsFeatureRequested("vix_zscore_20") ||
      IsFeatureRequested("us10yr_change_1") ||
      IsFeatureRequested("us10yr_zscore_20") ||
      IsFeatureRequested("usdx_change_1") ||
      IsFeatureRequested("usdx_zscore_20") ||
      IsFeatureRequested("nvda_xnas_log_return_1") ||
      IsFeatureRequested("aapl_xnas_log_return_1") ||
      IsFeatureRequested("msft_xnas_log_return_1") ||
      IsFeatureRequested("amzn_xnas_log_return_1") ||
      IsFeatureRequested("mega8_equal_return_1") ||
      IsFeatureRequested("top3_weighted_return_1") ||
      IsFeatureRequested("mega8_pos_breadth_1") ||
      IsFeatureRequested("mega8_dispersion_5") ||
      IsFeatureRequested("us100_minus_mega8_equal_return_1") ||
      IsFeatureRequested("us100_minus_top3_weighted_return_1");

   if(needs_external_block)
   {
      const datetime target_close_utc = rates[t].time + PeriodSeconds(PERIOD_M5);
      const int external_bars_needed = 25;

      MqlRates vix_rates[];
      MqlRates us10yr_rates[];
      MqlRates usdx_rates[];
      if(!LoadExternalSymbolRatesAligned("VIX", external_bars_needed, target_close_utc, vix_rates, skip_reason))
         return false;
      if(!LoadExternalSymbolRatesAligned("US10YR", external_bars_needed, target_close_utc, us10yr_rates, skip_reason))
         return false;
      if(!LoadExternalSymbolRatesAligned("USDX", external_bars_needed, target_close_utc, usdx_rates, skip_reason))
         return false;

      double vix_close_values[];
      double us10yr_close_values[];
      double usdx_close_values[];
      ArrayResize(vix_close_values, total_bars);
      ArrayResize(us10yr_close_values, total_bars);
      ArrayResize(usdx_close_values, total_bars);
      for(int i = 0; i < external_bars_needed; i++)
      {
         vix_close_values[i] = vix_rates[i].close;
         us10yr_close_values[i] = us10yr_rates[i].close;
         usdx_close_values[i] = usdx_rates[i].close;
      }

      value_vix_change_1 = SafeDivideValue(vix_close_values[external_bars_needed - 1], vix_close_values[external_bars_needed - 2]) - 1.0;
      value_vix_zscore_20 = RollingZscoreCurrent(vix_close_values, external_bars_needed, 20);
      value_us10yr_change_1 = SafeDivideValue(us10yr_close_values[external_bars_needed - 1], us10yr_close_values[external_bars_needed - 2]) - 1.0;
      value_us10yr_zscore_20 = RollingZscoreCurrent(us10yr_close_values, external_bars_needed, 20);
      value_usdx_change_1 = SafeDivideValue(usdx_close_values[external_bars_needed - 1], usdx_close_values[external_bars_needed - 2]) - 1.0;
      value_usdx_zscore_20 = RollingZscoreCurrent(usdx_close_values, external_bars_needed, 20);

      const int mega8_count = 8;
      string mega8_symbols[8];
      mega8_symbols[0] = "AAPL.xnas";
      mega8_symbols[1] = "AMZN.xnas";
      mega8_symbols[2] = "AMD.xnas";
      mega8_symbols[3] = "GOOGL.xnas";
      mega8_symbols[4] = "META.xnas";
      mega8_symbols[5] = "MSFT.xnas";
      mega8_symbols[6] = "NVDA.xnas";
      mega8_symbols[7] = "TSLA.xnas";

      double mega8_return_1_values[];
      double mega8_return_5_values[];
      ArrayResize(mega8_return_1_values, mega8_count);
      ArrayResize(mega8_return_5_values, mega8_count);

      for(int i = 0; i < mega8_count; i++)
      {
         MqlRates stock_rates[];
         if(!LoadExternalSymbolRatesAligned(mega8_symbols[i], external_bars_needed, target_close_utc, stock_rates, skip_reason))
            return false;

         const int ext_t = external_bars_needed - 1;
         const double simple_return_1 = SafeDivideValue(stock_rates[ext_t].close, stock_rates[ext_t - 1].close) - 1.0;
         const double simple_return_5 = SafeDivideValue(stock_rates[ext_t].close, stock_rates[ext_t - 5].close) - 1.0;
         mega8_return_1_values[i] = simple_return_1;
         mega8_return_5_values[i] = simple_return_5;

         if(mega8_symbols[i] == "AAPL.xnas")
            value_aapl_xnas_log_return_1 = MathLog(stock_rates[ext_t].close / stock_rates[ext_t - 1].close);
         else if(mega8_symbols[i] == "AMZN.xnas")
            value_amzn_xnas_log_return_1 = MathLog(stock_rates[ext_t].close / stock_rates[ext_t - 1].close);
         else if(mega8_symbols[i] == "MSFT.xnas")
            value_msft_xnas_log_return_1 = MathLog(stock_rates[ext_t].close / stock_rates[ext_t - 1].close);
         else if(mega8_symbols[i] == "NVDA.xnas")
            value_nvda_xnas_log_return_1 = MathLog(stock_rates[ext_t].close / stock_rates[ext_t - 1].close);
      }

      value_mega8_equal_return_1 = RollingMeanSlice(mega8_return_1_values, 0, mega8_count);
      value_top3_weighted_return_1 =
         (mega8_return_1_values[5] * OP_TOP3_EQUAL_WEIGHT) +
         (mega8_return_1_values[6] * OP_TOP3_EQUAL_WEIGHT) +
         (mega8_return_1_values[0] * OP_TOP3_EQUAL_WEIGHT);

      int positive_returns = 0;
      for(int i = 0; i < mega8_count; i++)
      {
         if(mega8_return_1_values[i] > 0.0)
            positive_returns++;
      }
      value_mega8_pos_breadth_1 = (double)positive_returns / mega8_count;
      value_mega8_dispersion_5 = PopulationStdSlice(mega8_return_5_values, 0, mega8_count);
      value_us100_minus_mega8_equal_return_1 = value_us100_simple_return_1 - value_mega8_equal_return_1;
      value_us100_minus_top3_weighted_return_1 = value_us100_simple_return_1 - value_top3_weighted_return_1;
   }

   const datetime expected_bar_close = rates[t].time + PeriodSeconds(PERIOD_M5);
   if(expected_bar_close != 0 && expected_bar_close != iTime(_Symbol, PERIOD_M5, 1) + PeriodSeconds(PERIOD_M5))
   {
      skip_reason = "PRICE_CORE_BAR_MISMATCH";
      return false;
   }

   const int active_feature_name_count = ArraySize(g_effective_feature_names);
   if(active_feature_name_count != g_effective_feature_count || g_effective_feature_count <= 0)
   {
      features[OP_IDX_LOG_RETURN_1] = value_log_return_1;
      features[OP_IDX_LOG_RETURN_3] = value_log_return_3;
      features[OP_IDX_HL_RANGE] = value_hl_range;
      features[OP_IDX_CLOSE_OPEN_RATIO] = value_close_open_ratio;
      features[OP_IDX_GAP_PERCENT] = value_gap_percent;
      features[OP_IDX_CLOSE_PREV_CLOSE_RATIO] = value_close_prev_close_ratio;
      features[OP_IDX_RETURN_ZSCORE_20] = value_return_zscore_20;
      features[OP_IDX_HL_ZSCORE_50] = value_hl_zscore_50;
      features[OP_IDX_ROC_12] = value_roc_12;
      features[OP_IDX_HISTORICAL_VOL_20] = value_historical_vol_20;
      features[OP_IDX_HISTORICAL_VOL_5_OVER_20] = value_historical_vol_5_over_20;
   }

   if(active_feature_name_count == g_effective_feature_count && g_effective_feature_count > 0)
   {
      for(int i = 0; i < g_effective_feature_count; i++)
         features[i] = 0.0;

      feature_ready_count = 0;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "log_return_1", value_log_return_1, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "log_return_3", value_log_return_3, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "hl_range", value_hl_range, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "close_open_ratio", value_close_open_ratio, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "gap_percent", value_gap_percent, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "close_prev_close_ratio", value_close_prev_close_ratio, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "return_zscore_20", value_return_zscore_20, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "hl_zscore_50", value_hl_zscore_50, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "overnight_return", value_overnight_return, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "return_1_over_atr_14", value_return_1_over_atr_14, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "close_ema20_ratio", value_close_ema20_ratio, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "close_ema50_ratio", value_close_ema50_ratio, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "ema9_ema20_diff", value_ema9_ema20_diff, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "ema20_ema50_diff", value_ema20_ema50_diff, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "ema50_ema200_diff", value_ema50_ema200_diff, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "ema20_ema50_spread_zscore_50", value_ema20_ema50_spread_zscore_50, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "sma50_sma200_ratio", value_sma50_sma200_ratio, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "rsi_14", value_rsi_14, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "rsi_50", value_rsi_50, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "rsi_14_slope_3", value_rsi_14_slope_3, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "rsi_14_minus_50", value_rsi_14_minus_50, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "stoch_kd_diff", value_stoch_kd_diff, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "stochrsi_kd_diff", value_stochrsi_kd_diff, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "ppo_hist_12_26_9", value_ppo_hist_12_26_9, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "roc_12", value_roc_12, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "trix_15", value_trix_15, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "atr_14", value_atr_14, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "atr_50", value_atr_50, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "atr_14_over_atr_50", value_atr_14_over_atr_50, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "bollinger_width_20", value_bollinger_width_20, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "bb_position_20", value_bb_position_20, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "bb_squeeze", value_bb_squeeze, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "historical_vol_20", value_historical_vol_20, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "historical_vol_5_over_20", value_historical_vol_5_over_20, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "adx_14", value_adx_14, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "di_spread_14", value_di_spread_14, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "supertrend_10_3", value_supertrend_10_3, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "vortex_indicator", value_vortex_indicator, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "is_us_cash_open", value_is_us_cash_open, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "minutes_from_cash_open", value_minutes_from_cash_open, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "is_first_30m_after_open", value_is_first_30m_after_open, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "is_last_30m_before_cash_close", value_is_last_30m_before_cash_close, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "vix_change_1", value_vix_change_1, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "vix_zscore_20", value_vix_zscore_20, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "us10yr_change_1", value_us10yr_change_1, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "us10yr_zscore_20", value_us10yr_zscore_20, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "usdx_change_1", value_usdx_change_1, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "usdx_zscore_20", value_usdx_zscore_20, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "nvda_xnas_log_return_1", value_nvda_xnas_log_return_1, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "aapl_xnas_log_return_1", value_aapl_xnas_log_return_1, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "msft_xnas_log_return_1", value_msft_xnas_log_return_1, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "amzn_xnas_log_return_1", value_amzn_xnas_log_return_1, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "mega8_equal_return_1", value_mega8_equal_return_1, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "top3_weighted_return_1", value_top3_weighted_return_1, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "mega8_pos_breadth_1", value_mega8_pos_breadth_1, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "mega8_dispersion_5", value_mega8_dispersion_5, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "us100_minus_mega8_equal_return_1", value_us100_minus_mega8_equal_return_1, skip_reason))
         return false;
      if(!TryAssignActiveFeatureValue(features, feature_ready_count, "us100_minus_top3_weighted_return_1", value_us100_minus_top3_weighted_return_1, skip_reason))
         return false;

      feature_vector_complete = (feature_ready_count == g_effective_feature_count);
      return true;
   }

   for(int idx = 0; idx < OP_FEATURE_COUNT; idx++)
   {
      if(idx == OP_IDX_LOG_RETURN_1 ||
         idx == OP_IDX_LOG_RETURN_3 ||
         idx == OP_IDX_HL_RANGE ||
         idx == OP_IDX_CLOSE_OPEN_RATIO ||
         idx == OP_IDX_GAP_PERCENT ||
         idx == OP_IDX_CLOSE_PREV_CLOSE_RATIO ||
         idx == OP_IDX_RETURN_ZSCORE_20 ||
         idx == OP_IDX_HL_ZSCORE_50 ||
         idx == OP_IDX_ROC_12 ||
         idx == OP_IDX_HISTORICAL_VOL_20 ||
         idx == OP_IDX_HISTORICAL_VOL_5_OVER_20)
      {
         if(!IsUsableValue(features[idx]))
         {
            skip_reason = StringFormat("PRICE_CORE_INVALID_%d", idx);
            return false;
         }
      }
   }

   feature_ready_count = OP_PRICE_CORE_READY_COUNT;
   feature_vector_complete = false;
   return true;
}

bool AuditFeatureVector(const double &features[], string &skip_reason)
{
   const int feature_count = ArraySize(features);
   if(feature_count != g_effective_feature_count)
   {
      skip_reason = StringFormat("FEATURE_COUNT_MISMATCH_%d", feature_count);
      return false;
   }

   for(int i = 0; i < feature_count; i++)
   {
      double value = features[i];
      if(!MathIsValidNumber(value) || MathAbs(value) >= (EMPTY_VALUE / 2.0))
      {
         skip_reason = StringFormat("FEATURE_INVALID_%d", i);
         return false;
      }
   }

   return true;
}

bool BuildStage1FeatureVector(
   const datetime bar_time_server,
   double &features[],
   string &feature_mode,
   int &feature_ready_count,
   bool &feature_vector_complete,
   string &skip_reason
)
{
   feature_mode = FeatureModeToString(InpFeatureMode);
   ArrayResize(features, g_effective_feature_count);
   feature_ready_count = 0;
   feature_vector_complete = false;
   for(int i = 0; i < g_effective_feature_count; i++)
      features[i] = 0.0;

   if(InpFeatureMode == OP_FEATURE_MODE_ZERO_SMOKE)
   {
      feature_ready_count = g_effective_feature_count;
      feature_vector_complete = true;
      return true;
   }

   if(InpFeatureMode == OP_FEATURE_MODE_PRICE_CORE_PARTIAL)
   {
      if(g_effective_feature_count != OP_FEATURE_COUNT && ArraySize(g_effective_feature_names) != g_effective_feature_count)
      {
         skip_reason = "FEATURE_SCHEMA_NAMES_NOT_READY";
         return false;
      }
      return BuildPriceCorePartialFeatures(features, feature_ready_count, feature_vector_complete, skip_reason);
   }

   skip_reason = "FEATURE_BUILDER_NOT_IMPLEMENTED";
   return false;
}

bool BuildInputTensor(const double &features[])
{
   if(ArraySize(features) != g_effective_feature_count)
      return false;

   ArrayResize(g_input_tensor, g_effective_feature_count);
   for(int i = 0; i < g_effective_feature_count; i++)
      g_input_tensor[i] = (float)features[i];
   return true;
}

bool RunInference(const double &features[], float &outputs[], string &skip_reason)
{
   if(g_onnx_handle == INVALID_HANDLE)
   {
      skip_reason = "MODEL_HANDLE_INVALID";
      return false;
   }

   if(!BuildInputTensor(features))
   {
      skip_reason = "INPUT_TENSOR_BUILD_FAIL";
      return false;
   }

   ArrayResize(g_output_tensor, OP_OUTPUT_COUNT);
   ArrayInitialize(g_output_tensor, 0.0);

   ResetLastError();
   if(!OnnxRun(g_onnx_handle, g_onnx_run_flags, g_input_tensor, g_output_tensor))
   {
      skip_reason = StringFormat("ONNX_RUN_FAIL_%d", GetLastError());
      return false;
   }

   ArrayResize(outputs, OP_OUTPUT_COUNT);
   for(int i = 0; i < OP_OUTPUT_COUNT; i++)
   {
      double value = (double)g_output_tensor[i];
      if(!MathIsValidNumber(value) || MathAbs(value) >= (EMPTY_VALUE / 2.0))
      {
         skip_reason = StringFormat("OUTPUT_INVALID_%d", i);
         return false;
      }
      outputs[i] = g_output_tensor[i];
   }

   return true;
}

bool PassDirectionFilters(
   const double p_short,
   const double p_flat,
   const double p_long,
   const int direction,
   string &filter_reason
)
{
   double selected = 0.0;
   double comparator = 0.0;
   double opposing_direction = 0.0;

   if(direction > 0)
   {
      selected = p_long;
      comparator = MathMax(p_short, p_flat);
      opposing_direction = p_short;
   }
   else
   {
      selected = p_short;
      comparator = MathMax(p_long, p_flat);
      opposing_direction = p_long;
   }

   if(g_effective_margin_rule_enabled)
   {
      if((selected - comparator) < g_effective_min_margin)
      {
         filter_reason = (direction > 0) ? "LONG_MARGIN_FAIL" : "SHORT_MARGIN_FAIL";
         return false;
      }
   }

   if(g_effective_prob_diff_rule_enabled)
   {
      if((selected - opposing_direction) < g_effective_min_probability_diff)
      {
         filter_reason = (direction > 0) ? "LONG_DIFF_FAIL" : "SHORT_DIFF_FAIL";
         return false;
      }
   }

   return true;
}

int DecideShadowSignal(const float &outputs[], string &decision_reason)
{
   if(ArraySize(outputs) < OP_OUTPUT_COUNT)
   {
      decision_reason = "OUTPUT_SIZE_INVALID";
      return 0;
   }

   const double p_short = (double)outputs[0];
   const double p_flat  = (double)outputs[1];
   const double p_long  = (double)outputs[2];

   if(!g_effective_threshold_rule_enabled)
   {
      decision_reason = "ENTRY_RULE_DISABLED";
      return 0;
   }

   const bool short_candidate = (p_short >= g_effective_short_threshold);
   const bool long_candidate  = (p_long >= g_effective_long_threshold);

   if(short_candidate && !long_candidate)
   {
      if(PassDirectionFilters(p_short, p_flat, p_long, -1, decision_reason))
      {
         decision_reason = "SHORT_FILTERS_OK";
         return -1;
      }
      return 0;
   }

   if(long_candidate && !short_candidate)
   {
      if(PassDirectionFilters(p_short, p_flat, p_long, 1, decision_reason))
      {
         decision_reason = "LONG_FILTERS_OK";
         return 1;
      }
      return 0;
   }

   if(short_candidate && long_candidate)
   {
      if(p_long > p_short && PassDirectionFilters(p_short, p_flat, p_long, 1, decision_reason))
      {
         decision_reason = "DUAL_SIGNAL_LONG_WINS";
         return 1;
      }
      if(p_short > p_long && PassDirectionFilters(p_short, p_flat, p_long, -1, decision_reason))
      {
         decision_reason = "DUAL_SIGNAL_SHORT_WINS";
         return -1;
      }

      decision_reason = "DUAL_SIGNAL_TIE_OR_MARGIN_FAIL";
      return 0;
   }

   decision_reason = "THRESHOLD_FAIL";
   return 0;
}

bool CheckRuntimeReady(string &skip_reason)
{
   if(_Symbol != "US100")
   {
      skip_reason = "SYMBOL_NOT_US100";
      return false;
   }

   if(_Period != PERIOD_M5)
   {
      skip_reason = "TIMEFRAME_NOT_M5";
      return false;
   }

   if(Bars(_Symbol, PERIOD_M5) < InpWarmupBars)
   {
      skip_reason = "WARMUP_NOT_READY";
      return false;
   }

   if(!g_shadow_ready || g_onnx_handle == INVALID_HANDLE)
   {
      skip_reason = "MODEL_NOT_READY";
      return false;
   }

   return true;
}

bool DumpModelIoSummary()
{
   if(!InpDumpModelIo || g_onnx_handle == INVALID_HANDLE)
      return true;

   const long input_count = OnnxGetInputCount(g_onnx_handle);
   const long output_count = OnnxGetOutputCount(g_onnx_handle);
   Log(StringFormat("ONNX io counts inputs=%d outputs=%d", (int)input_count, (int)output_count));

   if(input_count > 0)
      Log(StringFormat("ONNX input[0] name=%s", OnnxGetInputName(g_onnx_handle, 0)));
   if(output_count > 0)
      Log(StringFormat("ONNX output[0] name=%s", OnnxGetOutputName(g_onnx_handle, 0)));

   return true;
}

bool LoadShadowModel()
{
   ArrayResize(g_input_shape, 2);
   g_input_shape[0] = 1;
   g_input_shape[1] = (ulong)g_effective_feature_count;

   ArrayResize(g_output_shape, 2);
   g_output_shape[0] = 1;
   g_output_shape[1] = OP_OUTPUT_COUNT;

   uint create_flags = 0;
   if(InpOnnxUseCommonFiles)
      create_flags |= ONNX_COMMON_FOLDER;
   if(g_effective_onnx_use_common_files)
      create_flags |= ONNX_COMMON_FOLDER;

   g_onnx_run_flags = 0;
   if(InpUseCpuOnly)
      g_onnx_run_flags |= ONNX_USE_CPU_ONLY;

   ResetLastError();
   g_onnx_handle = OnnxCreate(g_effective_onnx_model_path, create_flags);
   if(g_onnx_handle == INVALID_HANDLE)
   {
      Log(StringFormat("OnnxCreate failed err=%d path=%s", GetLastError(), g_effective_onnx_model_path));
      return false;
   }

   ResetLastError();
   if(!OnnxSetInputShape(g_onnx_handle, 0, g_input_shape))
   {
      Log(StringFormat("OnnxSetInputShape failed err=%d", GetLastError()));
      OnnxRelease(g_onnx_handle);
      g_onnx_handle = INVALID_HANDLE;
      return false;
   }

   ResetLastError();
   if(!OnnxSetOutputShape(g_onnx_handle, 0, g_output_shape))
      Log(StringFormat("OnnxSetOutputShape warning err=%d; continuing with smoke validation", GetLastError()));

   ArrayResize(g_input_tensor, g_effective_feature_count);
   ArrayResize(g_output_tensor, OP_OUTPUT_COUNT);
   ArrayInitialize(g_input_tensor, 0.0);
   ArrayInitialize(g_output_tensor, 0.0);

   DumpModelIoSummary();
   g_shadow_ready = true;
   return true;
}

void ReleaseShadowModel()
{
   if(g_onnx_handle != INVALID_HANDLE)
   {
      OnnxRelease(g_onnx_handle);
      g_onnx_handle = INVALID_HANDLE;
   }
   g_shadow_ready = false;
}

bool DetectNewClosedBar(datetime &bar_time_server)
{
   bar_time_server = 0;
   const datetime current_bar_open = iTime(_Symbol, PERIOD_M5, 0);
   if(current_bar_open <= 0)
      return false;

   if(g_last_chart_bar_open == 0)
   {
      g_last_chart_bar_open = current_bar_open;
      return false;
   }

   if(current_bar_open == g_last_chart_bar_open)
      return false;

   g_last_chart_bar_open = current_bar_open;
   bar_time_server = iTime(_Symbol, PERIOD_M5, 1) + PeriodSeconds(PERIOD_M5);
   return (bar_time_server > 0);
}

bool SelectManagedPosition()
{
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      const ulong ticket = PositionGetTicket(i);
      if(ticket == 0)
         continue;
      if(!PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != _Symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != InpMagicNumber)
         continue;
      return true;
   }
   return false;
}

int CountManagedPositions()
{
   int count = 0;
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      const ulong ticket = PositionGetTicket(i);
      if(ticket == 0)
         continue;
      if(!PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != _Symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != InpMagicNumber)
         continue;
      count++;
   }
   return count;
}

void ResetManagedTradeTracking()
{
   g_managed_trade_active = false;
   g_managed_position_ticket = 0;
   g_managed_position_identifier = 0;
   g_managed_position_type = -1;
   g_managed_entry_time_server = 0;
   g_managed_entry_bar_time_server = 0;
   g_managed_entry_deal_ticket = 0;
   g_managed_entry_price = 0.0;
   g_managed_entry_volume = 0.0;
   g_managed_max_floating_profit = 0.0;
   g_managed_min_floating_profit = 0.0;
   g_managed_entry_decision = 0;
   g_managed_entry_decision_text = "";
   g_managed_sizing_mode = "";
   g_managed_stop_policy = "";
   g_managed_risk_context = "";
   g_managed_initial_stop_price = 0.0;
   g_managed_initial_stop_distance_price = 0.0;
   g_managed_initial_risk_amount = 0.0;
   g_managed_risk_pct_multiplier = 1.0;
   g_managed_stop_atr_mult_applied = 0.0;
   g_managed_peak_favorable_points = 0.0;
   const int exit_rule_count = ArraySize(g_effective_exit_rule_types);
   ArrayResize(g_managed_exit_rule_triggered, exit_rule_count);
   for(int i = 0; i < exit_rule_count; i++)
      g_managed_exit_rule_triggered[i] = false;
}

void UpdateManagedTradeTrackingFromSelectedPosition()
{
   if(!g_managed_trade_active)
      return;

   const double current_profit = PositionGetDouble(POSITION_PROFIT);
   if(!IsUsableValue(current_profit))
      return;

   if(current_profit > g_managed_max_floating_profit)
      g_managed_max_floating_profit = current_profit;
   if(current_profit < g_managed_min_floating_profit)
      g_managed_min_floating_profit = current_profit;
}

bool InitializeManagedTradeTracking(
   const datetime bar_time_server,
   const int decision,
   const ulong entry_deal_ticket,
   const double initial_stop_price,
   const double initial_stop_distance_price,
   const double initial_risk_amount,
   const double initial_risk_pct_multiplier,
   const string risk_context,
   const string stop_policy,
   const double stop_atr_mult_applied,
   const string sizing_mode
)
{
   if(!SelectManagedPosition())
      return false;

   g_managed_trade_active = true;
   g_managed_position_ticket = (ulong)PositionGetInteger(POSITION_TICKET);
   g_managed_position_identifier = (long)PositionGetInteger(POSITION_IDENTIFIER);
   g_managed_position_type = (long)PositionGetInteger(POSITION_TYPE);
   g_managed_entry_time_server = (datetime)PositionGetInteger(POSITION_TIME);
   g_managed_entry_bar_time_server = bar_time_server;
   g_managed_entry_deal_ticket = entry_deal_ticket;
   g_managed_entry_price = PositionGetDouble(POSITION_PRICE_OPEN);
   g_managed_entry_volume = PositionGetDouble(POSITION_VOLUME);
   g_managed_entry_decision = decision;
   g_managed_entry_decision_text = DecisionToString(decision);

   const double initial_profit = PositionGetDouble(POSITION_PROFIT);
   g_managed_max_floating_profit = IsUsableValue(initial_profit) ? initial_profit : 0.0;
   g_managed_min_floating_profit = IsUsableValue(initial_profit) ? initial_profit : 0.0;
   g_managed_sizing_mode = sizing_mode;
   g_managed_stop_policy = stop_policy;
   g_managed_risk_context = risk_context;
   g_managed_initial_stop_price = initial_stop_price;
   g_managed_initial_stop_distance_price = initial_stop_distance_price;
   g_managed_initial_risk_amount = initial_risk_amount;
   g_managed_risk_pct_multiplier = initial_risk_pct_multiplier;
   g_managed_stop_atr_mult_applied = stop_atr_mult_applied;
   g_managed_peak_favorable_points = 0.0;
   const int exit_rule_count = ArraySize(g_effective_exit_rule_types);
   ArrayResize(g_managed_exit_rule_triggered, exit_rule_count);
   for(int i = 0; i < exit_rule_count; i++)
      g_managed_exit_rule_triggered[i] = false;
   return true;
}

bool ComputeManagedPositionPointState(
   MqlTick &tick,
   double &current_favorable_points,
   double &current_adverse_points,
   double &current_close_price
)
{
   current_favorable_points = 0.0;
   current_adverse_points = 0.0;
   current_close_price = 0.0;

   ResetLastError();
   if(!SymbolInfoTick(_Symbol, tick))
      return false;

   if(g_managed_position_type == POSITION_TYPE_BUY)
   {
      current_close_price = tick.bid;
      current_favorable_points = current_close_price - g_managed_entry_price;
      current_adverse_points = g_managed_entry_price - current_close_price;
   }
   else if(g_managed_position_type == POSITION_TYPE_SELL)
   {
      current_close_price = tick.ask;
      current_favorable_points = g_managed_entry_price - current_close_price;
      current_adverse_points = current_close_price - g_managed_entry_price;
   }
   else
   {
      return false;
   }

   if(current_adverse_points < 0.0)
      current_adverse_points = 0.0;
   return true;
}

void RefreshManagedTrackingAfterPartialClose()
{
   if(!SelectManagedPosition())
      return;

   g_managed_position_ticket = (ulong)PositionGetInteger(POSITION_TICKET);
   g_managed_position_identifier = (long)PositionGetInteger(POSITION_IDENTIFIER);
   g_managed_position_type = (long)PositionGetInteger(POSITION_TYPE);
   g_managed_entry_volume = PositionGetDouble(POSITION_VOLUME);

   const double current_profit = PositionGetDouble(POSITION_PROFIT);
   g_managed_max_floating_profit = IsUsableValue(current_profit) ? current_profit : 0.0;
   g_managed_min_floating_profit = IsUsableValue(current_profit) ? current_profit : 0.0;
   g_managed_peak_favorable_points = 0.0;

   MqlTick tick;
   double favorable_points = 0.0;
   double adverse_points = 0.0;
   double close_price = 0.0;
   if(ComputeManagedPositionPointState(tick, favorable_points, adverse_points, close_price) && favorable_points > 0.0)
      g_managed_peak_favorable_points = favorable_points;
}

bool ExecuteManagedFullClose(const string close_reason, const datetime exit_bar_time_server, string &action_reason)
{
   ResetLastError();
   if(!g_trade.PositionClose(_Symbol, InpTradeDeviationPoints))
   {
      action_reason = StringFormat("%s_CLOSE_FAIL_%d", close_reason, GetLastError());
      return false;
   }

   const ulong close_deal_ticket = g_trade.ResultDeal();
   if(!AppendClosedTradeLedger(close_reason, exit_bar_time_server, close_deal_ticket))
      Log(StringFormat("trade ledger append failed after %s", close_reason));

   ResetManagedTradeTracking();
   g_entry_block_bar_time = exit_bar_time_server;
   action_reason = close_reason + "_CLOSE_OK";
   return true;
}

double ResolvePartialCloseVolume(const double current_volume, const double close_fraction)
{
   if(close_fraction <= 0.0 || close_fraction >= 1.0)
      return 0.0;

   const double close_volume = NormalizeVolumeForSymbol(current_volume * close_fraction);
   if(close_volume <= 0.0)
      return 0.0;

   const double remaining_volume = NormalizeVolumeForSymbol(current_volume - close_volume);
   const double min_volume = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   if(remaining_volume <= 0.0)
      return 0.0;
   if(min_volume > 0.0 && remaining_volume + 1e-9 < min_volume)
      return 0.0;
   return close_volume;
}

bool ExecuteManagedPartialClose(
   const int rule_index,
   const string close_reason,
   const double close_fraction,
   const datetime exit_bar_time_server,
   string &action_reason
)
{
   if(!SelectManagedPosition())
      return true;

   const double current_volume = PositionGetDouble(POSITION_VOLUME);
   const double close_volume = ResolvePartialCloseVolume(current_volume, close_fraction);
   if(close_volume <= 0.0)
   {
      action_reason = close_reason + "_PARTIAL_VOLUME_UNAVAILABLE";
      return true;
   }

   ResetLastError();
   if(!g_trade.PositionClosePartial(_Symbol, close_volume, InpTradeDeviationPoints))
   {
      action_reason = StringFormat("%s_PARTIAL_FAIL_%d", close_reason, GetLastError());
      return false;
   }

   const ulong close_deal_ticket = g_trade.ResultDeal();
   if(!AppendClosedTradeLedger(close_reason, exit_bar_time_server, close_deal_ticket))
      Log(StringFormat("trade ledger append failed after %s", close_reason));

   if(rule_index >= 0 && rule_index < ArraySize(g_managed_exit_rule_triggered))
      g_managed_exit_rule_triggered[rule_index] = true;

   if(SelectManagedPosition())
   {
      RefreshManagedTrackingAfterPartialClose();
      action_reason = close_reason + "_PARTIAL_OK";
      return true;
   }

   ResetManagedTradeTracking();
   g_entry_block_bar_time = exit_bar_time_server;
   action_reason = close_reason + "_PARTIAL_CLOSE_OK";
   return true;
}

bool ApplyManagedPointExitRules(const datetime current_bar_time_server, const int hold_bars, string &action_reason)
{
   const int exit_rule_count = ArraySize(g_effective_exit_rule_types);
   if(exit_rule_count <= 0)
      return true;

   bool has_point_rule = false;
   for(int i = 0; i < exit_rule_count; i++)
   {
      if(!g_effective_exit_rule_enabled[i])
         continue;
      const string rule_type = g_effective_exit_rule_types[i];
      if(rule_type == "break_even" ||
         rule_type == "trailing_stop" ||
         rule_type == "partial_stop_loss" ||
         rule_type == "partial_take_profit")
      {
         has_point_rule = true;
         break;
      }
   }

   if(!has_point_rule)
      return true;

   MqlTick tick;
   double favorable_points = 0.0;
   double adverse_points = 0.0;
   double close_price = 0.0;
   if(!ComputeManagedPositionPointState(tick, favorable_points, adverse_points, close_price))
   {
      action_reason = "POINT_EXIT_TICK_UNAVAILABLE";
      return false;
   }

   if(favorable_points > g_managed_peak_favorable_points)
      g_managed_peak_favorable_points = favorable_points;

   for(int i = 0; i < exit_rule_count; i++)
   {
      if(!g_effective_exit_rule_enabled[i])
         continue;
      if(i < ArraySize(g_managed_exit_rule_triggered) && g_managed_exit_rule_triggered[i])
         continue;
      if(g_effective_exit_rule_min_hold_bars[i] > 0 && hold_bars < g_effective_exit_rule_min_hold_bars[i])
         continue;

      const string rule_type = g_effective_exit_rule_types[i];
      if(rule_type == "break_even")
      {
         const double trigger_points = g_effective_exit_rule_trigger_points[i];
         const double offset_points = g_effective_exit_rule_offset_points[i];
         if(trigger_points > 0.0 &&
            g_managed_peak_favorable_points >= trigger_points &&
            favorable_points <= offset_points + 1e-6)
         {
            return ExecuteManagedFullClose("BREAK_EVEN_STOP", current_bar_time_server, action_reason);
         }
      }
      else if(rule_type == "trailing_stop")
      {
         const double trigger_points = g_effective_exit_rule_trigger_points[i];
         const double distance_points = g_effective_exit_rule_distance_points[i];
         if(trigger_points > 0.0 &&
            distance_points > 0.0 &&
            g_managed_peak_favorable_points >= trigger_points &&
            (g_managed_peak_favorable_points - favorable_points) >= distance_points - 1e-6)
         {
            return ExecuteManagedFullClose("TRAIL_STOP", current_bar_time_server, action_reason);
         }
      }
      else if(rule_type == "partial_stop_loss")
      {
         const double trigger_points = g_effective_exit_rule_trigger_points[i];
         const double close_fraction = g_effective_exit_rule_close_fraction[i];
         if(trigger_points > 0.0 &&
            close_fraction > 0.0 &&
            adverse_points >= trigger_points - 1e-6)
         {
            return ExecuteManagedPartialClose(i, "PARTIAL_STOP_LOSS", close_fraction, current_bar_time_server, action_reason);
         }
      }
      else if(rule_type == "partial_take_profit")
      {
         const double trigger_points = g_effective_exit_rule_trigger_points[i];
         const double close_fraction = g_effective_exit_rule_close_fraction[i];
         if(trigger_points > 0.0 &&
            close_fraction > 0.0 &&
            favorable_points >= trigger_points - 1e-6)
         {
            return ExecuteManagedPartialClose(i, "PARTIAL_TAKE_PROFIT", close_fraction, current_bar_time_server, action_reason);
         }
      }
   }

   return true;
}

bool AppendClosedTradeLedger(const string close_reason, const datetime exit_bar_time_server, const ulong close_deal_ticket)
{
   if(!InpWriteTradeLedger || !g_managed_trade_active)
      return true;
   if(!EnsureTradeLedgerHeader())
      return false;

   if(close_deal_ticket == 0)
   {
      Log("trade ledger close deal ticket missing");
      return false;
   }

   if(!HistorySelect(g_managed_entry_time_server - 86400, TimeCurrent() + 60))
   {
      Log(StringFormat("trade ledger history select failed err=%d", GetLastError()));
      return false;
   }

   const double exit_price = HistoryDealGetDouble(close_deal_ticket, DEAL_PRICE);
   const double exit_volume = HistoryDealGetDouble(close_deal_ticket, DEAL_VOLUME);
   const datetime exit_time_server = (datetime)HistoryDealGetInteger(close_deal_ticket, DEAL_TIME);
   const double gross_profit = HistoryDealGetDouble(close_deal_ticket, DEAL_PROFIT);
   const double swap = HistoryDealGetDouble(close_deal_ticket, DEAL_SWAP);
   const double commission = HistoryDealGetDouble(close_deal_ticket, DEAL_COMMISSION);
   const double fee = HistoryDealGetDouble(close_deal_ticket, DEAL_FEE);
   const double net_profit = gross_profit + swap + commission + fee;
   const int hold_bars = (g_managed_entry_bar_time_server > 0 && exit_bar_time_server >= g_managed_entry_bar_time_server)
      ? (int)((exit_bar_time_server - g_managed_entry_bar_time_server) / PeriodSeconds(PERIOD_M5))
      : 0;
   const double initial_stop_distance_points = (g_managed_initial_stop_distance_price > 0.0 && _Point > 0.0)
      ? (g_managed_initial_stop_distance_price / _Point)
      : EMPTY_VALUE;
   const double realized_r_multiple = (g_managed_initial_risk_amount > 0.0)
      ? (net_profit / g_managed_initial_risk_amount)
      : EMPTY_VALUE;

   int flags = FILE_READ | FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(InpTradeLedgerUseCommonFiles)
      flags |= FILE_COMMON;

   int handle = FileOpen(InpTradeLedgerPath, flags);
   if(handle == INVALID_HANDLE)
   {
      Log(StringFormat("failed to append trade ledger err=%d path=%s", GetLastError(), InpTradeLedgerPath));
      return false;
   }

   FileSeek(handle, 0, SEEK_END);

   string line =
      EscapeCsv(TimeToString(TimeGMT(), TIME_DATE | TIME_SECONDS)) + "," +
      EscapeCsv(_Symbol) + "," +
      EscapeCsv((string)g_managed_position_ticket) + "," +
      EscapeCsv((string)g_managed_position_identifier) + "," +
      EscapeCsv(g_managed_entry_decision_text) + "," +
      EscapeCsv(CsvDouble((exit_volume > 0.0) ? exit_volume : g_managed_entry_volume, 2)) + "," +
      EscapeCsv(TimeToString(g_managed_entry_time_server, TIME_DATE | TIME_SECONDS)) + "," +
      EscapeCsv(TimeToString(exit_time_server, TIME_DATE | TIME_SECONDS)) + "," +
      EscapeCsv(TimeToString(g_managed_entry_bar_time_server, TIME_DATE | TIME_SECONDS)) + "," +
      EscapeCsv(TimeToString(exit_bar_time_server, TIME_DATE | TIME_SECONDS)) + "," +
      EscapeCsv(CsvDouble(g_managed_entry_price, 5)) + "," +
      EscapeCsv(CsvDouble(exit_price, 5)) + "," +
      EscapeCsv((string)hold_bars) + "," +
      EscapeCsv(close_reason) + "," +
      EscapeCsv(g_managed_entry_decision_text) + "," +
      EscapeCsv(g_managed_sizing_mode) + "," +
      EscapeCsv(g_managed_stop_policy) + "," +
      EscapeCsv(CsvDouble(g_managed_risk_pct_multiplier, 4)) + "," +
      EscapeCsv(g_managed_risk_context) + "," +
      EscapeCsv(CsvDouble(g_managed_stop_atr_mult_applied, 4)) + "," +
      EscapeCsv(CsvDouble(g_managed_initial_stop_price, 5)) + "," +
      EscapeCsv(CsvDouble(initial_stop_distance_points, 2)) + "," +
      EscapeCsv(CsvDouble(g_managed_initial_risk_amount, 2)) + "," +
      EscapeCsv(CsvDouble(realized_r_multiple, 4)) + "," +
      EscapeCsv(CsvDouble(gross_profit, 2)) + "," +
      EscapeCsv(CsvDouble(swap, 2)) + "," +
      EscapeCsv(CsvDouble(commission, 2)) + "," +
      EscapeCsv(CsvDouble(fee, 2)) + "," +
      EscapeCsv(CsvDouble(net_profit, 2)) + "," +
      EscapeCsv(CsvDouble(g_managed_max_floating_profit, 2)) + "," +
      EscapeCsv(CsvDouble(g_managed_min_floating_profit, 2));

   FileWriteString(handle, line + "\r\n");
   FileClose(handle);
   return true;
}

bool ManageOpenPositionOnTick(string &action_reason)
{
   action_reason = "";
   if(!InpEnableTrading)
      return true;

   if(!SelectManagedPosition())
   {
      if(g_managed_trade_active)
      {
         ulong close_deal_ticket = 0;
         string close_reason = "";
         datetime exit_bar_time_server = 0;
         if(ResolveManagedCloseDealFromHistory(close_deal_ticket, close_reason, exit_bar_time_server))
         {
            if(!AppendClosedTradeLedger(close_reason, exit_bar_time_server, close_deal_ticket))
               Log("trade ledger append failed after broker-native close");
            g_entry_block_bar_time = exit_bar_time_server;
            action_reason = close_reason;
         }
         ResetManagedTradeTracking();
      }
      return true;
   }

   UpdateManagedTradeTrackingFromSelectedPosition();

   const datetime position_time = (datetime)PositionGetInteger(POSITION_TIME);
   const int entry_bar_shift = iBarShift(_Symbol, PERIOD_M5, position_time, false);
   if(entry_bar_shift < 0)
   {
      action_reason = "POSITION_BAR_SHIFT_INVALID";
      return true;
   }

   if(g_effective_stop_execution_mode != "broker_native" && g_managed_initial_stop_price > 0.0)
   {
      MqlTick tick;
      if(!SymbolInfoTick(_Symbol, tick))
      {
         action_reason = "HARD_STOP_TICK_UNAVAILABLE";
         return false;
      }

      bool hard_stop_hit = false;
      if(g_managed_position_type == POSITION_TYPE_BUY && tick.bid <= g_managed_initial_stop_price)
         hard_stop_hit = true;
      else if(g_managed_position_type == POSITION_TYPE_SELL && tick.ask >= g_managed_initial_stop_price)
         hard_stop_hit = true;

      if(hard_stop_hit)
      {
         ResetLastError();
         if(!g_trade.PositionClose(_Symbol, InpTradeDeviationPoints))
         {
            action_reason = StringFormat("HARD_STOP_CLOSE_FAIL_%d", GetLastError());
            return false;
         }

         const datetime current_bar_open = iTime(_Symbol, PERIOD_M5, 0);
         const datetime exit_bar_time_server = current_bar_open + PeriodSeconds(PERIOD_M5);
         const ulong close_deal_ticket = g_trade.ResultDeal();
         if(!AppendClosedTradeLedger("HARD_STOP", exit_bar_time_server, close_deal_ticket))
            Log("trade ledger append failed after hard stop");

         ResetManagedTradeTracking();
         g_entry_block_bar_time = exit_bar_time_server;
         action_reason = "HARD_STOP_CLOSE_OK";
         return true;
      }
   }

   const datetime current_bar_time_server = iTime(_Symbol, PERIOD_M5, 0) + PeriodSeconds(PERIOD_M5);
   const int hold_bars = (g_managed_entry_bar_time_server > 0 && current_bar_time_server >= g_managed_entry_bar_time_server)
      ? (int)((current_bar_time_server - g_managed_entry_bar_time_server) / PeriodSeconds(PERIOD_M5))
      : 0;
   if(!ApplyManagedPointExitRules(current_bar_time_server, hold_bars, action_reason))
      return false;
   if(StringLen(action_reason) > 0)
      return true;

   if(!g_effective_time_exit_enabled)
      return true;

   string hold_context = "BASE";
   const int effective_max_hold_bars = ResolveDynamicMaxHoldBars(current_bar_time_server, hold_context);
   if(entry_bar_shift < effective_max_hold_bars)
      return true;

   ResetLastError();
   if(!g_trade.PositionClose(_Symbol, InpTradeDeviationPoints))
   {
      action_reason = StringFormat("TIME_EXIT_CLOSE_FAIL_%d", GetLastError());
      return false;
   }

   const datetime exit_bar_time_server = iTime(_Symbol, PERIOD_M5, 1) + PeriodSeconds(PERIOD_M5);
   const ulong close_deal_ticket = g_trade.ResultDeal();
   string time_exit_close_reason = "TIME_EXIT";
   if(hold_context != "BASE")
      time_exit_close_reason = "TIME_EXIT_" + hold_context;
   if(!AppendClosedTradeLedger(time_exit_close_reason, exit_bar_time_server, close_deal_ticket))
      Log("trade ledger append failed after time exit");

   ResetManagedTradeTracking();
   g_entry_block_bar_time = exit_bar_time_server;
   action_reason = "TIME_EXIT_CLOSE_OK";
   return true;
}

bool ManageOpenPositionOnNewBar(
   const datetime bar_time_server,
   const double p_short,
   const double p_flat,
   const double p_long,
   string &action_reason
)
{
   action_reason = "";
   if(!InpEnableTrading || !g_effective_flat_exit_enabled)
      return true;

   if(!SelectManagedPosition())
      return true;

   if(!g_managed_trade_active)
      return true;

   if(g_managed_entry_bar_time_server <= 0)
      return true;

   const int hold_bars = (int)((bar_time_server - g_managed_entry_bar_time_server) / PeriodSeconds(PERIOD_M5));
   if(hold_bars < g_effective_flat_exit_min_hold_bars)
      return true;

   if(p_flat < g_effective_flat_exit_min_probability)
      return true;

   ResetLastError();
   if(!g_trade.PositionClose(_Symbol, InpTradeDeviationPoints))
   {
      action_reason = StringFormat("FLAT_EXIT_CLOSE_FAIL_%d", GetLastError());
      return false;
   }

   const ulong close_deal_ticket = g_trade.ResultDeal();
   if(!AppendClosedTradeLedger("FLAT_EXIT", bar_time_server, close_deal_ticket))
      Log("trade ledger append failed after flat exit");

   ResetManagedTradeTracking();
   g_entry_block_bar_time = bar_time_server;
   action_reason = StringFormat(
      "FLAT_EXIT_CLOSE_OK_%.3f_%.3f_%.3f",
      p_short,
      p_flat,
      p_long
   );
   return true;
}

bool ExecuteTradeDecision(const int decision, const datetime bar_time_server, string &action_reason)
{
   action_reason = "";
   g_last_trade_fill_price = 0.0;
   if(!InpEnableTrading)
      return true;

   if(bar_time_server > g_entry_block_bar_time)
      g_entry_block_bar_time = 0;

   if(decision == 0)
   {
      action_reason = "NO_ENTRY_SIGNAL";
      return true;
   }

   if(g_entry_block_bar_time == bar_time_server)
   {
      action_reason = "ENTRY_BLOCKED_AFTER_EXIT";
      return true;
   }

   if(CountManagedPositions() >= g_effective_max_concurrent_positions)
   {
      action_reason = "POSITION_ALREADY_OPEN";
      return true;
   }

   double planned_volume = 0.0;
   double planned_stop_price = 0.0;
   double planned_stop_distance_price = 0.0;
   double planned_stop_atr_mult = 0.0;
   double planned_risk_amount = 0.0;
   double planned_risk_pct_multiplier = 1.0;
   string planned_risk_context = "BASE";
   string plan_reason = "";
   if(!ComputeTradeExecutionPlan(
      decision,
      bar_time_server,
      planned_volume,
      planned_stop_price,
      planned_stop_distance_price,
      planned_stop_atr_mult,
      planned_risk_amount,
      planned_risk_pct_multiplier,
      planned_risk_context,
      plan_reason
   ))
   {
      action_reason = plan_reason;
      return false;
   }
   if(planned_volume <= 0.0)
   {
      action_reason = plan_reason;
      return true;
   }

   ResetLastError();
   bool trade_ok = false;
   string comment = StringFormat("OP|%s|%s", g_effective_experiment_id, DecisionToString(decision));
   double broker_stop_price = 0.0;
   if(g_effective_sizing_mode == "risk_pct" && g_effective_stop_execution_mode == "broker_native")
      broker_stop_price = planned_stop_price;
   if(decision > 0)
      trade_ok = g_trade.Buy(planned_volume, _Symbol, 0.0, broker_stop_price, 0.0, comment);
   else
      trade_ok = g_trade.Sell(planned_volume, _Symbol, 0.0, broker_stop_price, 0.0, comment);

   if(!trade_ok)
   {
      action_reason = StringFormat("ENTRY_ORDER_FAIL_%d", GetLastError());
      return false;
   }

   g_last_trade_fill_price = g_trade.ResultPrice();
   double applied_stop_price = 0.0;
   double applied_stop_distance_price = planned_stop_distance_price;
   double applied_risk_amount = 0.0;
   if(g_effective_sizing_mode == "risk_pct" && planned_stop_distance_price > 0.0)
   {
      applied_stop_price = (decision > 0)
         ? (g_last_trade_fill_price - planned_stop_distance_price)
         : (g_last_trade_fill_price + planned_stop_distance_price);
      applied_stop_price = NormalizePriceForSymbol(applied_stop_price);

      if(g_effective_stop_execution_mode == "broker_native" && SelectManagedPosition())
      {
         const double position_sl = PositionGetDouble(POSITION_SL);
         if(IsUsableValue(position_sl) && position_sl > 0.0)
         {
            applied_stop_price = position_sl;
            applied_stop_distance_price = MathAbs(g_last_trade_fill_price - applied_stop_price);
         }
      }

      double loss_per_lot = 0.0;
      string loss_reason = "";
      if(ComputeLossPerLotAtStop(decision, g_last_trade_fill_price, applied_stop_price, loss_per_lot, loss_reason))
         applied_risk_amount = loss_per_lot * planned_volume;
      else
         Log(StringFormat("risk recompute failed after entry: %s", loss_reason));
   }

   if(!InitializeManagedTradeTracking(
      bar_time_server,
      decision,
      g_trade.ResultDeal(),
      applied_stop_price,
      applied_stop_distance_price,
      applied_risk_amount,
      planned_risk_pct_multiplier,
      planned_risk_context,
      g_effective_stop_policy,
      planned_stop_atr_mult,
      g_effective_sizing_mode
   ))
      Log("managed trade tracking initialization failed after entry");

   action_reason = StringFormat(
      "%s_VOL_%.4f_STOP_%.5f_RISK_%.2f_STOPMODE_%s_STOPPOLICY_%s_STOPMULT_%.4f",
      (decision > 0) ? "ENTRY_BUY_OK" : "ENTRY_SELL_OK",
      planned_volume,
      applied_stop_price,
      applied_risk_amount,
      g_effective_stop_execution_mode,
      g_effective_stop_policy,
      planned_stop_atr_mult
   );
   return true;
}

bool RunShadowCycle(const datetime bar_time_server, const string cycle_tag)
{
   ResetExternalAlignmentTelemetry();
   string feature_mode = FeatureModeToString(InpFeatureMode);
   string skip_reason = "";
   string decision_reason = "SKIPPED";
   string trade_action_reason = "";
   string planned_risk_context = "SKIPPED";
   double features[];
   float outputs[];
   ulong feature_checksum = 0;
   double p_short = 0.0;
   double p_flat = 0.0;
   double p_long = 0.0;
   double planned_risk_pct_multiplier = 1.0;
   bool row_ready = false;
   bool feature_vector_complete = false;
   int feature_ready_count = 0;
   int decision = 0;

   if(!CheckRuntimeReady(skip_reason))
   {
      RecordGovernanceObservation(skip_reason, false, p_short, p_flat, p_long, decision, planned_risk_context, planned_risk_pct_multiplier);
      AppendShadowLog(bar_time_server, feature_mode, feature_ready_count, false, skip_reason, feature_checksum, p_short, p_flat, p_long, DecisionToString(decision), decision_reason, cycle_tag, "", 0.0);
      AppendGovernanceLog(bar_time_server, cycle_tag, false, skip_reason, DecisionToString(decision), decision_reason, "", p_short, p_flat, p_long, false);
      Log(StringFormat("%s skipped: %s", cycle_tag, skip_reason));
      return false;
   }

   if(!BuildStage1FeatureVector(bar_time_server, features, feature_mode, feature_ready_count, feature_vector_complete, skip_reason))
   {
      RecordGovernanceObservation(skip_reason, false, p_short, p_flat, p_long, decision, planned_risk_context, planned_risk_pct_multiplier);
      AppendShadowLog(bar_time_server, feature_mode, feature_ready_count, false, skip_reason, feature_checksum, p_short, p_flat, p_long, DecisionToString(decision), decision_reason, cycle_tag, "", 0.0);
      AppendGovernanceLog(bar_time_server, cycle_tag, false, skip_reason, DecisionToString(decision), decision_reason, "", p_short, p_flat, p_long, false);
      Log(StringFormat("%s skipped: %s", cycle_tag, skip_reason));
      return false;
   }

   if(!AuditFeatureVector(features, skip_reason))
   {
      RecordGovernanceObservation(skip_reason, false, p_short, p_flat, p_long, decision, planned_risk_context, planned_risk_pct_multiplier);
      AppendShadowLog(bar_time_server, feature_mode, feature_ready_count, false, skip_reason, feature_checksum, p_short, p_flat, p_long, DecisionToString(decision), decision_reason, cycle_tag, "", 0.0);
      AppendGovernanceLog(bar_time_server, cycle_tag, false, skip_reason, DecisionToString(decision), decision_reason, "", p_short, p_flat, p_long, false);
      Log(StringFormat("%s skipped: %s", cycle_tag, skip_reason));
      return false;
   }

   feature_checksum = ComputeFeatureChecksum(features);

   if(!feature_vector_complete && !InpAllowPartialInference)
   {
      skip_reason = "PARTIAL_FEATURE_VECTOR";
      decision_reason = "INFERENCE_SKIPPED";
      RecordGovernanceObservation(skip_reason, false, p_short, p_flat, p_long, decision, planned_risk_context, planned_risk_pct_multiplier);
      AppendShadowLog(bar_time_server, feature_mode, feature_ready_count, false, skip_reason, feature_checksum, p_short, p_flat, p_long, DecisionToString(decision), decision_reason, cycle_tag, "", 0.0);
      AppendGovernanceLog(bar_time_server, cycle_tag, false, skip_reason, DecisionToString(decision), decision_reason, "", p_short, p_flat, p_long, false);
      Log(StringFormat("%s skipped: %s mode=%s ready=%d", cycle_tag, skip_reason, feature_mode, feature_ready_count));
      return false;
   }

   if(!RunInference(features, outputs, skip_reason))
   {
      RecordGovernanceObservation(skip_reason, false, p_short, p_flat, p_long, decision, planned_risk_context, planned_risk_pct_multiplier);
      AppendShadowLog(bar_time_server, feature_mode, feature_ready_count, false, skip_reason, feature_checksum, p_short, p_flat, p_long, DecisionToString(decision), decision_reason, cycle_tag, "", 0.0);
      AppendGovernanceLog(bar_time_server, cycle_tag, false, skip_reason, DecisionToString(decision), decision_reason, "", p_short, p_flat, p_long, false);
      Log(StringFormat("%s inference failed: %s", cycle_tag, skip_reason));
      return false;
   }

   p_short = (double)outputs[0];
   p_flat = (double)outputs[1];
   p_long = (double)outputs[2];

   decision = DecideShadowSignal(outputs, decision_reason);
   row_ready = true;
   if(decision != 0)
      planned_risk_pct_multiplier = ResolveDynamicRiskPctMultiplier(decision, bar_time_server, planned_risk_context);
   else
      planned_risk_context = "NO_SIGNAL";

   string exit_action_reason = "";
   if(!ManageOpenPositionOnNewBar(bar_time_server, p_short, p_flat, p_long, exit_action_reason))
      Log(StringFormat("%s exit action failed: %s", cycle_tag, exit_action_reason));
   else if(InpEnableTrading && exit_action_reason != "")
      Log(StringFormat("%s exit action: %s", cycle_tag, exit_action_reason));

   RecordGovernanceObservation(skip_reason, true, p_short, p_flat, p_long, decision, planned_risk_context, planned_risk_pct_multiplier);

   string entry_action_reason = "";
   bool entry_blocked_this_bar = false;
   if(InpEnableTrading && decision != 0 && g_governance_entry_blocked)
   {
      entry_blocked_this_bar = true;
      entry_action_reason = "ENTRY_BLOCKED_GOVERNANCE_" + g_governance_reason;
      Log(StringFormat("%s governance blocked entry: %s", cycle_tag, g_governance_reason));
   }
   else if(!ExecuteTradeDecision(decision, bar_time_server, entry_action_reason))
      Log(StringFormat("%s trade action failed: %s", cycle_tag, entry_action_reason));
   else if(InpEnableTrading && entry_action_reason != "" && entry_action_reason != "NO_ENTRY_SIGNAL")
      Log(StringFormat("%s trade action: %s", cycle_tag, entry_action_reason));

   if(exit_action_reason != "" && entry_action_reason != "")
      trade_action_reason = exit_action_reason + "|" + entry_action_reason;
   else if(exit_action_reason != "")
      trade_action_reason = exit_action_reason;
   else
      trade_action_reason = entry_action_reason;
   AppendShadowLog(bar_time_server, feature_mode, feature_ready_count, row_ready, "", feature_checksum, p_short, p_flat, p_long, DecisionToString(decision), decision_reason, cycle_tag, trade_action_reason, g_last_trade_fill_price);
   AppendGovernanceLog(bar_time_server, cycle_tag, row_ready, "", DecisionToString(decision), decision_reason, trade_action_reason, p_short, p_flat, p_long, entry_blocked_this_bar);

   Log(StringFormat(
      "%s bar=%s mode=%s ready=%d p_short=%.6f p_flat=%.6f p_long=%.6f decision=%s reason=%s",
      cycle_tag,
      TimeToString(bar_time_server, TIME_DATE | TIME_SECONDS),
      feature_mode,
      feature_ready_count,
      p_short,
      p_flat,
      p_long,
      DecisionToString(decision),
      decision_reason
   ));
   return true;
}

int OnInit()
{
   if(_Symbol != "US100")
   {
      Log("attach this EA to US100 only");
      return INIT_PARAMETERS_INCORRECT;
   }

   if(_Period != PERIOD_M5)
   {
      Log("attach this EA to PERIOD_M5 only");
      return INIT_PARAMETERS_INCORRECT;
   }

   if(InpWarmupBars < 50)
   {
      Log("InpWarmupBars must be at least 50");
      return INIT_PARAMETERS_INCORRECT;
   }

   if(InpEnableGovernance)
   {
      if(InpGovernanceWindowBars <= 0)
      {
         Log("InpGovernanceWindowBars must be positive");
         return INIT_PARAMETERS_INCORRECT;
      }
      if(InpGovernanceMinSamples <= 0 || InpGovernanceMinSamples > InpGovernanceWindowBars)
      {
         Log("InpGovernanceMinSamples must be between 1 and InpGovernanceWindowBars");
         return INIT_PARAMETERS_INCORRECT;
      }
      if(InpGovernanceMaxOperationalSkipRate < 0.0 || InpGovernanceMaxOperationalSkipRate > 1.0 ||
         InpGovernanceMaxExternalSkipRate < 0.0 || InpGovernanceMaxExternalSkipRate > 1.0 ||
         InpGovernanceMaxFeatureSkipRate < 0.0 || InpGovernanceMaxFeatureSkipRate > 1.0 ||
         InpGovernanceMaxArgmaxClassShare < 0.0 || InpGovernanceMaxArgmaxClassShare > 1.0 ||
         InpGovernanceMaxExtremeConfidenceRate < 0.0 || InpGovernanceMaxExtremeConfidenceRate > 1.0 ||
         InpGovernanceExtremeConfidenceThreshold < 0.0 || InpGovernanceExtremeConfidenceThreshold > 1.0 ||
         InpGovernanceMinNormalizedEntropy < 0.0 || InpGovernanceMinNormalizedEntropy > 1.0)
      {
         Log("governance rate thresholds must stay within [0,1]");
         return INIT_PARAMETERS_INCORRECT;
      }
      if(InpGovernanceMaxConsecutiveOperationalSkips <= 0)
      {
         Log("InpGovernanceMaxConsecutiveOperationalSkips must be positive");
         return INIT_PARAMETERS_INCORRECT;
      }
   }

   if(!LoadRuntimeConfig())
      return INIT_FAILED;

   ResetManagedTradeTracking();
   ResetGovernanceState();
   EnsureLogHeader();
   EnsureTradeLedgerHeader();
   EnsureGovernanceLogHeader();
   g_trade.SetExpertMagicNumber((ulong)InpMagicNumber);
   g_trade.SetDeviationInPoints(InpTradeDeviationPoints);

    if(!CreateIndicatorHandles())
      return INIT_FAILED;

   if(!LoadShadowModel())
   {
      ReleaseIndicatorHandles();
      return INIT_FAILED;
   }

   g_last_chart_bar_open = iTime(_Symbol, PERIOD_M5, 0);

   if(InpRunSmokeOnInit)
   {
      const datetime smoke_bar_time = iTime(_Symbol, PERIOD_M5, 1) + PeriodSeconds(PERIOD_M5);
      RunShadowCycle(smoke_bar_time, "INIT_SMOKE");
   }

   Log("Stage 1 shadow EA initialized");
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   ReleaseShadowModel();
   ReleaseIndicatorHandles();
   Log(StringFormat("Stage 1 shadow EA deinitialized reason=%d", reason));
}

void OnTick()
{
   string manage_reason = "";
   if(!ManageOpenPositionOnTick(manage_reason))
      Log(StringFormat("tick position management failed: %s", manage_reason));
   else if(InpEnableTrading && manage_reason == "TIME_EXIT_CLOSE_OK")
      Log("tick position management: TIME_EXIT_CLOSE_OK");

   datetime bar_time_server = 0;
   if(!DetectNewClosedBar(bar_time_server))
      return;

   RunShadowCycle(bar_time_server, "NEW_BAR");
}
