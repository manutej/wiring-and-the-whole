public class LoansController {
  public Page list(int p) { return svc.fetchPage(p); }
  public Dto get(long id) { return svc.fetchOne(id); }
  void log(String m) { audit.log(m); }
  // refs: loans.LoansService#fetchPage loans.LoansService#fetchOne shared.AuditDto#log shared.PageDto#of
}
